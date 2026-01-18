from cProfile import label
from turtle import width
from typing import Literal, Union, List
import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go

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
    
class Bond:
    def __init__(
        self,
        face_value: float = 1000,
        quantity: int = 1
    ):
        self.face_value = face_value
        self.quantity = quantity

    def payoff(self, spot_prices):
        return np.full_like(spot_prices, self.face_value * self.quantity)
            

class Payoff_Diagram:
    def __init__(
        self,
        portfolio: List,
    ):
        self.portfolio = portfolio

st.title("Option Portfolio Payoff Diagram")

spot_range = np.linspace(0, 50, 11)

portfolio = []
payoffs = []




portfolio.append(Bond(-10))
portfolio.append(Option('put', strike=30, quantity=1))
portfolio.append(Option('call', strike=30, quantity=-1))
portfolio.append(Option('call', strike=20, quantity=-1))





# initialize total_payoff
total_payoff = np.zeros_like(spot_range)

for i, asset in enumerate(portfolio):
    payoff = asset.payoff(spot_range)
    payoffs.append(payoff)
    total_payoff += payoffs[i]

df = pd.DataFrame({
    'Spot Price': spot_range,
    # 'Option 1': payoff1,
    # 'Option 2': payoff2,
    'Total Payoff': total_payoff
})
df = df.set_index('Spot Price')

# Create plotly figure
fig = go.Figure()

# Add total payoff line
fig.add_trace(go.Scatter(
    x=spot_range,
    y=total_payoff,
    mode='lines',
    name='Total Payoff',
    line=dict(color='#ff4b4b', width=3)
))

# Update layout for dark mode
fig.update_layout(
    title="Option Portfolio Payoff Diagram",
    xaxis_title="Spot Price",
    yaxis_title="Payoff ($)",
    xaxis=dict(range=[0, 50], dtick=5, gridcolor='rgba(128,128,128,0.2)'),
    yaxis=dict(range=[-50, 50], dtick=5, gridcolor='rgba(128,128,128,0.2)'),
    plot_bgcolor='#0e1117',
    paper_bgcolor='#0e1117',
    font=dict(color='white'),
    hovermode='x unified'
)

# Add zero line
fig.add_hline(y=0, line_color='gray', line_width=1, opacity=0.5)

st.plotly_chart(fig, use_container_width=True)