import streamlit as st
import pandas as pd
from utils import Option, Debt
from styling import apply_page_config

apply_page_config("Portfolio Input", "📊")


# Initialize portfolio in session state if needed
if 'portfolio' not in st.session_state:
    st.session_state.portfolio = []

st.title("📊 Portfolio Input & Management")

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