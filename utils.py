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
        self.strike = face_value  # For dynamic range calculation

    def payoff(self, spot_prices):
        return np.full_like(spot_prices, self.face_value)