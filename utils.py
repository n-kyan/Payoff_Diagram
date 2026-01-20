from typing import Literal
import numpy as np

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
    
class Debt:
    def __init__(self, face_value: float):
        self.face_value = face_value
        self.strike = face_value

    def payoff(self, spot_prices):
        return np.full_like(spot_prices, self.face_value)
    
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

    
def simulate_terminal_prices(spot: float, expected_drift: float, volatility: float, time_horizon: float, num_simulations: int) -> np.ndarray:
    
    # Step 1: Sample ε from standard normal N(0,1)
    epsilon = np.random.standard_normal(num_simulations)
    
    # Step 2: Calculate the exponent: (μ - σ²/2)T + σε√T
    exponent = (expected_drift - 0.5 * volatility**2) * time_horizon + volatility * epsilon * np.sqrt(time_horizon)
    
    # Step 3: Calculate S_T = S₀ · exp[exponent]
    terminal_prices = spot * np.exp(exponent)
    
    return terminal_prices
