import streamlit as st
from styling import apply_page_config

apply_page_config("Option Portfolio Analyzer", "📊")

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

# Initialize session state for portfolio
if 'portfolio' not in st.session_state:
    st.session_state.portfolio = []

st.title("📊 Option Portfolio Analyzer")

st.write("""
### Welcome to the Option Portfolio Analyzer

This application provides comprehensive tools for analyzing option portfolios:

- **📊 Portfolio Input**: Build and manage your option portfolio
- **📈 Payoff Diagram**: Visualize payoff structures at expiration
- **📉 PnL Distribution**: Simulate profit and loss distributions

👈 **Get started by selecting a page from the sidebar**
""")

# Optional: Show quick portfolio summary if exists
if len(st.session_state.portfolio) > 0:
    st.success(f"Current portfolio contains {len(st.session_state.portfolio)} position(s)")
else:
    st.info("No portfolio loaded. Start by adding positions in the Portfolio Input page.")