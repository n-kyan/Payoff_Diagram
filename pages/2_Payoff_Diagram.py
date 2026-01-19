import streamlit as st
import numpy as np
import plotly.graph_objects as go
from styling import apply_page_config

if 'portfolio' not in st.session_state: st.session_state.portfolio = []
apply_page_config("Payoff Diagram")


st.title("Payoff Diagram Analysis")


# Settings
spot_range = [90, 110]
num_points = 21
y_range = [-20, 20]

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
        title="Portfolio Payoff Diagram",
        height=600,
        xaxis_title="Spot Price",
        yaxis_title="Payoff ($)",
        xaxis=dict(range=[spot_range[0], spot_range[1]], gridcolor='rgba(128,128,128,0.2)',
        dtick=1,
        showgrid=True),
        yaxis=dict(range=y_range, gridcolor='rgba(128,128,128,0.2)'),
        plot_bgcolor='#0e1117',
        paper_bgcolor='#0e1117',
        font=dict(color='white'),
        hovermode='x unified'
    )
    
    # Add zero line
    fig.add_hline(y=0, line_color='white', line_width=1, opacity=.5)
    
    st.plotly_chart(fig, use_container_width=True)
else:
    st.info("No portfolio loaded.")

