import streamlit as st
from styling import apply_page_config

if 'portfolio' not in st.session_state: st.session_state.portfolio = []
apply_page_config("Home")

st.title("Option Portfolio Analyzer")
st.divider()

st.write("### Pages")
col1, col2, col3 = st.columns(3)

with col1:
    st.page_link("pages/1_Portfolio_Input.py", label="**Portfolio Input**", icon="🔗")
    st.write("Build and manage your option portfolio")

with col2:
    st.page_link("pages/2_Payoff_Diagram.py", label="**Payoff Diagram**", icon="🔗")
    st.write("Visualize payoff structures at expiration")

with col3:
    st.page_link("pages/3_PnL_Distribution.py", label="**PnL Distribution**", icon="🔗")
    st.write("Simulate profit and loss distributions")

# Optional: Show quick portfolio summary if exists
if len(st.session_state.portfolio) > 0:
    st.success(f"Current portfolio contains {len(st.session_state.portfolio)} position(s)")