from typing import Literal, Union, List
import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(layout="wide", page_title="Option Portfolio Analyzer")

# Hide Streamlit branding
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

# Sidebar navigation
with st.sidebar:
    st.title("Navigation")
    page = st.radio(
        "Select Page",
        ["Portfolio Input", "Payoff Diagram", "PnL Distribution"],
        label_visibility="collapsed"
    )

# ============================================================================
# PORTFOLIO INPUT PAGE
# ============================================================================
if page == "Portfolio Input":
    st.title("Portfolio Input & Details")
    
    # Main area split: Upload section + Portfolio table
    upload_col, details_col = st.columns([1, 2])
    
    with upload_col:
        st.subheader("Add Assets")
        
        # CSV Upload option
        st.write("**Import from CSV**")
        uploaded_file = st.file_uploader("Upload Portfolio CSV", type=['csv'])
        if uploaded_file is not None:
            # TODO: Implement CSV parsing
            st.info("CSV upload functionality coming soon!")
        
        st.divider()
        
        # Manual input
        st.write("**Manual Entry**")
        asset_type = st.selectbox("Asset Type", ["Option", "Debt"])
        
        if asset_type == "Option":
            option_type = st.selectbox("Option Type", ["call", "put"])
            strike = st.number_input("Strike Price", value=100.0, step=1.0)
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
    
    with details_col:
        st.subheader("Current Portfolio")
        
        if len(st.session_state.portfolio) > 0:
            # Create portfolio table
            portfolio_data = []
            
            for i, asset in enumerate(st.session_state.portfolio):
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
            
            df_portfolio = pd.DataFrame(portfolio_data)
            st.dataframe(df_portfolio, use_container_width=True, hide_index=True)
            
            # Clear portfolio button
            if st.button("Clear Portfolio", type="secondary"):
                st.session_state.portfolio = []
                st.rerun()
        else:
            st.info("No assets in portfolio yet. Add assets using the panel on the left.")

# ============================================================================
# PAYOFF DIAGRAM PAGE
# ============================================================================
elif page == "Payoff Diagram":
    st.title("Payoff Diagram Analysis")
    
    # Main chart area + settings column
    chart_col, settings_col = st.columns([3, 1])
    
    with settings_col:
        st.subheader("Display Settings")
        
        # Spot range settings
        spot_range = st.slider(
            "Spot Price Range",
            min_value=0,
            max_value=100,
            value=(0, 50),
            step=5
        )
        
        num_points = st.number_input(
            "Number of Points",
            min_value=10,
            max_value=1000,
            value=11,
            step=10
        )
        
        y_range = st.slider(
            "Y-axis Range",
            min_value=-100,
            max_value=100,
            value=(-50, 50),
            step=5
        )
    
    with chart_col:
        if len(st.session_state.portfolio) > 0:
            # Create spot range
            spot_range_array = np.linspace(spot_range[0], spot_range[1], num_points)
            
            # Calculate total payoff
            total_payoff = np.zeros_like(spot_range_array)
            for asset in st.session_state.portfolio:
                payoff = asset.payoff(spot_range_array)
                total_payoff += payoff
            
            # Create plotly figure
            fig = go.Figure()
            
            fig.add_trace(go.Scatter(
                x=spot_range_array,
                y=total_payoff,
                mode='lines',
                name='Total Payoff',
                line=dict(color='#ff4b4b', width=3)
            ))
            
            # Update layout
            fig.update_layout(
                title="Option Portfolio Payoff Diagram",
                height=600,
                xaxis_title="Spot Price",
                yaxis_title="Payoff ($)",
                xaxis=dict(range=[spot_range[0], spot_range[1]], gridcolor='rgba(128,128,128,0.2)'),
                yaxis=dict(range=y_range, gridcolor='rgba(128,128,128,0.2)'),
                plot_bgcolor='#0e1117',
                paper_bgcolor='#0e1117',
                font=dict(color='white'),
                hovermode='x unified'
            )
            
            # Add zero line
            fig.add_hline(y=0, line_color='gray', line_width=1, opacity=0.5)
            
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No portfolio loaded. Please add assets on the Portfolio Input page.")

# ============================================================================
# PNL DISTRIBUTION PAGE
# ============================================================================
elif page == "PnL Distribution":
    st.title("PnL Distribution Analysis")
    
    # Main area + settings column
    main_col, settings_col = st.columns([3, 1])
    
    with settings_col:
        st.subheader("Simulation Settings")
        
        num_simulations = st.number_input(
            "Number of Simulations", 
            min_value=100, 
            max_value=100000, 
            value=10000, 
            step=1000
        )
        
        st.write("**Market Parameters**")
        spot = st.number_input("Spot Price", value=100.0, step=1.0)
        expected_drift = st.number_input("Expected Drift (μ)", value=0.05, step=0.01, format="%.2f")
        volatility = st.number_input("Volatility (σ)", value=0.20, step=0.01, format="%.2f")
        time_horizon = st.number_input("Time Horizon (years)", value=1.0, step=0.1, format="%.2f")
    
    with main_col:
        if len(st.session_state.portfolio) > 0:
            st.write("### Simulation Parameters")
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Spot Price", f"${spot:.2f}")
                st.metric("Expected Drift", f"{expected_drift*100:.1f}%")
            with col2:
                st.metric("Volatility", f"{volatility*100:.1f}%")
                st.metric("Simulations", f"{num_simulations:,}")
            
            # Placeholder for simulation
            st.info("Simulation functionality to be implemented")
        else:
            st.info("No portfolio loaded. Please add assets on the Portfolio Input page.")
# ```

# **Questions before we continue:**

# 1. Does this overall structure look good to you?
# 2. For the CSV upload, what format should we expect? Something like:
# ```
#    Type,Option_Type,Strike,Quantity,Face_Value
#    Option,call,100,1,
#    Option,put,95,-1,
#    Debt,,,,-10