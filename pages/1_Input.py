import streamlit as st
import pandas as pd
from styling import apply_page_config
from utils import Forward, Option, Debt

if 'portfolio' not in st.session_state:
    st.session_state.portfolio = []

apply_page_config("Portfolio Input")

st.title("Portfolio Input & Management")
st.divider()

col1, col2 = st.columns([3, 1])

with col1:
    st.subheader("Current Portfolio")
        
    if len(st.session_state.portfolio) > 0:
        # Create portfolio table
        portfolio_data = []
        
        for i, asset in enumerate(st.session_state.portfolio):
            if type(asset).__name__ == 'Option':
                portfolio_data.append({
                    'ID': i,
                    'Type': 'Option',
                    'Call/Put': asset.option_type.capitalize(),
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
            elif type(asset).__name__ == 'Forward':
                portfolio_data.append({
                    'ID': i,
                    'Type': 'Forward',
                    'Call/Put': '-',
                    'Strike': asset.strike,
                    'Quantity': asset.quantity,
                    'Spot': '-',
                    'Maturity': '-',
                    'RFR': '-',
                    'Volatility': '-',
                    'Face Value': '-'
                })
        
        df_portfolio = pd.DataFrame(portfolio_data)
        st.dataframe(df_portfolio, use_container_width=True, hide_index=True)
        
        if st.button("Clear Portfolio"):
            st.session_state.portfolio = []
            st.rerun()
    else:
        st.info("None.")

with col2:
    st.subheader("Add Assets")

    # Manual input
    st.write("**Manual Entry**")
    asset_type = st.pills(
        "Asset Type", 
        ["Option", "Debt", "Forward"],
        default="Option"  # Set default selection
    )

    if asset_type == "Option":
        option_type = st.pills(
            "Option Type", 
            ["Call", "Put"],
            default="Call"
        )
        strike = st.number_input("Strike Price", value=100, step=5)
        quantity = st.number_input("Quantity", value=1, step=1)
        
        if st.button("Add Option", use_container_width=True):
            new_option = Option(option_type.lower(), strike=strike, quantity=quantity)
            st.session_state.portfolio.append(new_option)
            st.rerun()

    # In the "Add Debt" section, replace with:
    elif asset_type == "Debt":
        face_value = st.number_input("Face Value", value=-10.0, step=5.0)
        
        if st.button("Add Debt", use_container_width=True):
            new_debt = Debt(
                face_value=face_value,
                maturity=1.0,  # Add default maturity
                rfr=0.05       # Add default rfr
            )
            st.session_state.portfolio.append(new_debt)
            st.rerun()

    elif asset_type == "Forward":
        strike = st.number_input("Strike Price", value=100, step=5)
        quantity = st.number_input("Quantity", value=1, step=1)

        if st.button("Add Forward", use_container_width=True):
            new_forward = Forward(
                strike=strike,
                spot=100.0,     # Add default spot
                maturity=1.0,   # Add default maturity
                rfr=0.05,       # Add default rfr
                quantity=quantity
            )
            st.session_state.portfolio.append(new_forward)
            st.rerun()


    st.divider()

    # CSV Upload option
    uploaded_file = st.file_uploader("**Upload CSV**", type=['csv'])
    if uploaded_file is not None:
        # TODO: Implement CSV parsing
        st.info("CSV upload functionality coming soon!")

