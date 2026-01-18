from typing import Literal, Union, List
import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(layout="wide", page_title="Option Portfolio Analyzer")

# Hide Streamlit branding and make full screen
st.markdown("""
    <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        .block-container {
            padding-top: 1rem;
            padding-bottom: 0rem;
        }
    </style>
    """, unsafe_allow_html=True)

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

# Initialize session state for portfolio
if 'portfolio' not in st.session_state:
    st.session_state.portfolio = []

# st.title("Option Portfolio Payoff Diagram")

# # Create two columns - main content and right panel
# col1, col2 = st.columns([3, 1])

# with col2:
#     with st.expander("➕ Add Assets", expanded=True):
#         asset_type = st.selectbox("Asset Type", ["Option", "Debt"])
        
#         if asset_type == "Option":
#             option_type = st.selectbox("Option Type", ["call", "put"])
#             strike = st.number_input("Strike Price", value=30.0, step=1.0)
#             quantity = st.number_input("Quantity", value=1, step=1)
            
#             if st.button("Add Option", use_container_width=True):
#                 new_option = Option(option_type, strike=strike, quantity=quantity)
#                 st.session_state.portfolio.append(new_option)
#                 st.rerun()
        
#         elif asset_type == "Debt":
#             face_value = st.number_input("Face Value", value=-10.0, step=1.0)
            
#             if st.button("Add Debt", use_container_width=True):
#                 new_debt = Debt(face_value=face_value)
#                 st.session_state.portfolio.append(new_debt)
#                 st.rerun()

# with col1:
#     # Get all strikes and create dynamic range
#     # strikes = [asset.strike for asset in st.session_state.portfolio if hasattr(asset, 'strike')]
    
#     # if strikes:
#     #     min_strike = min(strikes)
#     #     max_strike = max(strikes)
#     #     spot_range = np.linspace(min_strike * 0.5, max_strike * 1.5, 100)
#     # else:
#         # spot_range = np.linspace(0, 50, 100)

#     # Fixed range
#     spot_range = np.linspace(0, 50, 10)
    
#     # Calculate payoffs
#     payoffs = []
#     total_payoff = np.zeros_like(spot_range)
    
#     for asset in st.session_state.portfolio:
#         payoff = asset.payoff(spot_range)
#         payoffs.append(payoff)
#         total_payoff += payoff
    
#     # Create plotly figure
#     fig = go.Figure()
    
#     # Add total payoff line
#     fig.add_trace(go.Scatter(
#         x=spot_range,
#         y=total_payoff,
#         mode='lines',
#         name='Total Payoff',
#         line=dict(color='#ff4b4b', width=3)
#     ))
    
#     # Update layout for dark mode
#     y_min = min(total_payoff) * 1.2 if min(total_payoff) < 0 else -25
#     y_max = max(total_payoff) * 1.2 if max(total_payoff) > 0 else 25
    
#     fig.update_layout(
#         title="Option Portfolio Payoff Diagram",
#         height=600,
#         xaxis_title="Spot Price",
#         yaxis_title="Payoff ($)",
#         xaxis=dict(range=[spot_range[0], spot_range[-1]], dtick=5, gridcolor='rgba(128,128,128,0.2)'),
#         yaxis=dict(range=[y_min, y_max], dtick=5, gridcolor='rgba(128,128,128,0.2)'),
#         plot_bgcolor='#0e1117',
#         paper_bgcolor='#0e1117',
#         font=dict(color='white'),
#         hovermode='x unified'
#     )
    
#     # Add zero line
#     fig.add_hline(y=0, line_color='gray', line_width=1, opacity=0.5)
    
#     st.plotly_chart(fig, use_container_width=True)







st.title("Option Portfolio Analyzer")

# Create tabs
tab1, tab2 = st.tabs(["📈 Payoff Diagram", "📊 Portfolio Details"])

with tab1:
    # Create two columns - main content and right panel
    col1, col2 = st.columns([3, 1])

    with col2:
        with st.expander("➕ Add Assets", expanded=True):
            asset_type = st.selectbox("Asset Type", ["Option", "Debt"])
        
        if asset_type == "Option":
            option_type = st.selectbox("Option Type", ["call", "put"])
            strike = st.number_input("Strike Price", value=30.0, step=1.0)
            quantity = st.number_input("Quantity", value=1, step=1)
            
            if st.button("Add Option", use_container_width=True):
                new_option = Option(option_type, strike=strike, quantity=quantity)
                st.session_state.portfolio.append(new_option)
                st.rerun()
        
        elif asset_type == "Debt":
            face_value = st.number_input("Face Value", value=-10.0, step=1.0)
            
            if st.button("Add Debt", use_container_width=True):
                new_debt = Debt(face_value=face_value)
                st.session_state.portfolio.append(new_debt)
                st.rerun()
    
    with col1:
         # Get all strikes and create dynamic range
        # strikes = [asset.strike for asset in st.session_state.portfolio if hasattr(asset, 'strike')]
        
        # if strikes:
        #     min_strike = min(strikes)
        #     max_strike = max(strikes)
        #     spot_range = np.linspace(min_strike * 0.5, max_strike * 1.5, 100)
        # else:
            # spot_range = np.linspace(0, 50, 100)

        # Fixed range
        spot_range = np.linspace(0, 50, 11)
        
        # Calculate payoffs
        payoffs = []
        total_payoff = np.zeros_like(spot_range)
        
        for asset in st.session_state.portfolio:
            payoff = asset.payoff(spot_range)
            payoffs.append(payoff)
            total_payoff += payoff
        
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
        y_min = -50
        y_max = 50
        
        fig.update_layout(
            title="Option Portfolio Payoff Diagram",
            height=600,
            xaxis_title="Spot Price",
            yaxis_title="Payoff ($)",
            xaxis=dict(range=[spot_range[0], spot_range[-1]], dtick=5, gridcolor='rgba(128,128,128,0.2)'),
            yaxis=dict(range=[y_min, y_max], dtick=5, gridcolor='rgba(128,128,128,0.2)'),
            plot_bgcolor='#0e1117',
            paper_bgcolor='#0e1117',
            font=dict(color='white'),
            hovermode='x unified'
        )
        
        # Add zero line
        fig.add_hline(y=0, line_color='gray', line_width=1, opacity=0.5)
        
        st.plotly_chart(fig, use_container_width=True)

with tab2:
    st.header("Portfolio Details")
    
    if len(st.session_state.portfolio) > 0:
        # Debug: show what's actually in the portfolio
        # st.write("Debug - Portfolio contents:")
        # for i, asset in enumerate(st.session_state.portfolio):
        #     st.write(f"Asset {i}: {type(asset)} - {type(asset).__name__}")
        
        # Create data for the table
        portfolio_data = []
        
        for i, asset in enumerate(st.session_state.portfolio):
            # Use type name instead of isinstance
            if type(asset).__name__ == 'Option':
                portfolio_data.append({
                    'ID': i,
                    'Type': 'Option',
                    'Call/Put': asset.option_type,
                    'Strike': asset.strike,
                    'Quantity': asset.quantity,
                    'Spot': asset.spot,
                    'Maturity': asset.maturity,
                    'RFR': asset.rfr,
                    'Volatility': asset.volatility,
                    'Face Value': '-'
                })
            elif type(asset).__name__ == 'Debt':
                portfolio_data.append({
                    'ID': i,
                    'Type': 'Debt',
                    'Call/Put': '-',
                    'Strike': '-',
                    'Quantity': '-',
                    'Spot': '-',
                    'Maturity': '-',
                    'RFR': '-',
                    'Volatility': '-',
                    'Face Value': asset.face_value
                })
        
        # Create DataFrame
        df_portfolio = pd.DataFrame(portfolio_data)
        
        # Display table
        st.dataframe(df_portfolio, use_container_width=True, hide_index=True)
        
        # st.write(f"Portfolio data rows: {len(portfolio_data)}")
        
    else:
        st.info("No assets in portfolio yet")