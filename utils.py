from typing import Literal
import numpy as np
from scipy.stats import norm, skew, kurtosis

class Option:
    def __init__(
        self,
        option_type: Literal['call', 'put'],
        strike: float,
        spot: float = 100,
        maturity: float = 1,
        rfr: float = 0.12,
        volatility: float = 0.20,
        quantity: int = 1
    ):
        self.option_type = option_type.lower()
        self.strike = strike
        self.spot = spot
        self.maturity = maturity
        self.rfr = rfr
        self.volatility = volatility
        self.quantity = quantity
        self._validate_inputs()

    def _validate_inputs(self):
        if self.option_type not in ['call', 'put']:
            raise ValueError("option_type must be 'call' or 'put'")
        if self.strike <= 0:
            raise ValueError("Strike must be positive")
        if self.spot <= 0:
            raise ValueError("Spot must be positive")
        if self.maturity < 0:
            raise ValueError("Maturity must be non-negative")
        if self.volatility <= 0:
            raise ValueError("Volatility must be positive")
        
    def payoff(self, spot_prices):
        if self.option_type == 'call':
            payoff = np.maximum(spot_prices - self.strike, 0)
        else:  # put
            payoff = np.maximum(self.strike - spot_prices, 0)
        return payoff * self.quantity
    
    def price(self):

        if self.maturity == 0:
            return self.payoff(self.spot)[0] if isinstance(self.spot, np.ndarray) else self.payoff(np.array([self.spot]))[0]
        
        d1 = (np.log(self.spot / self.strike) + 
              (self.rfr + 0.5 * self.volatility**2) * self.maturity) / \
             (self.volatility * np.sqrt(self.maturity))
        
        d2 = d1 - self.volatility * np.sqrt(self.maturity)

        # N(d) is the cumulative normal distribution - it gives us probabilities
        if self.option_type == 'call':
            price = (self.spot * norm.cdf(d1) - 
                    self.strike * np.exp(-self.rfr * self.maturity) * norm.cdf(d2))
        else:  # put
            price = (self.strike * np.exp(-self.rfr * self.maturity) * norm.cdf(-d2) - 
                    self.spot * norm.cdf(-d1))
        
        return price * self.quantity
    
class Debt:
    def __init__(self, face_value: float):
        self.face_value = face_value
        self.strike = face_value

    def payoff(self, spot_prices):
        return np.full_like(spot_prices, self.face_value)
    
    def price(self, rfr=0.05, maturity=1.0):
        """Calculate present value - requires market parameters"""
        return self.face_value * np.exp(-rfr * maturity)
    
class Forward:
    def __init__(
        self,
        strike: float,
        quantity: int = 1
    ):
        self.strike = strike
        self.quantity = quantity
        self._validate_inputs()
    
    def _validate_inputs(self):
        if self.strike <= 0:
            raise ValueError("Strike must be positive")
    
    def payoff(self, spot_prices):
        return (spot_prices - self.strike) * self.quantity
    
    def price(self, spot=100, rfr=0.05, maturity=1.0):
        """Calculate present value - requires market parameters"""
        forward_price = spot * np.exp(rfr * maturity)
        return (forward_price - self.strike) * np.exp(-rfr * maturity) * self.quantity

    
def simulate_portfolio_pnl(
    portfolio: list,
    spot: float,
    expected_drift: float,
    volatility: float,
    maturity: float,
    rfr: float,
    num_simulations: int = 10000
) -> dict:
    # Calculate initial cost - pass parameters to price() methods
    initial_cost = 0
    for asset in portfolio:
        if hasattr(asset, 'price'):
            if type(asset).__name__ == 'Option':
                initial_cost += asset.price()  # Options have all params
            elif type(asset).__name__ == 'Forward':
                initial_cost += asset.price(spot=spot, rfr=rfr, maturity=maturity)
            elif type(asset).__name__ == 'Debt':
                initial_cost += asset.price(rfr=rfr, maturity=maturity)
    
    epsilon = np.random.standard_normal(num_simulations)
    exponent = ((expected_drift - 0.5 * volatility**2) * maturity + 
                volatility * epsilon * np.sqrt(maturity))
    terminal_prices = spot * np.exp(exponent)
    
    terminal_values = np.zeros(num_simulations)
    for asset in portfolio:
        terminal_values += asset.payoff(terminal_prices)
    
    future_cost = initial_cost * np.exp(rfr * maturity)
    pnl = terminal_values - future_cost
    
    from scipy.stats import skew, kurtosis
    
    return {
        'pnl_samples': pnl,
        'terminal_prices': terminal_prices,
        'initial_cost': initial_cost,
        'mean': np.mean(pnl),
        'std': np.std(pnl),
        'skew': skew(pnl),
        'kurtosis': kurtosis(pnl),
        'min': np.min(pnl),
        'max': np.max(pnl),
        'percentile_5': np.percentile(pnl, 5),
        'percentile_95': np.percentile(pnl, 95)
    }