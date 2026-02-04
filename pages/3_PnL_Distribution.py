import streamlit as st
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from styling import apply_page_config
from utils import simulate_portfolio_pnl

if 'portfolio' not in st.session_state:
    st.session_state.portfolio = []

apply_page_config("PnL Distribution")

st.title("PnL Distribution Analysis")
st.markdown("""
This page shows you the **probability distribution** of profit and loss for your portfolio.
Unlike the payoff diagram which shows all possible outcomes equally, this shows which 
outcomes are actually *likely* to occur based on how stocks actually move.
""")

# Main area + settings column
main_col, settings_col = st.columns([3, 1])

with settings_col:
    st.subheader("Simulation Settings")
    
    num_simulations = st.number_input(
        "Number of Simulations", 
        min_value=1000, 
        max_value=100000, 
        value=10000, 
        step=1000,
        help="More simulations = smoother histogram but slower computation"
    )
    
    st.write("**Market Parameters**")
    spot = st.number_input("Spot Price", value=100.0, step=1.0,
                          help="Current stock price")
    expected_drift = st.number_input("Expected Drift (μ)", value=0.05, step=0.01, format="%.2f",
                                     help="Your expected annual return on the stock")
    volatility = st.number_input("Volatility (σ)", value=0.20, step=0.01, format="%.2f",
                                help="Annual volatility of the stock")
    rfr = st.number_input("Risk-Free Rate", value=0.05, step=0.01, format="%.2f",
                         help="Annual risk-free interest rate")
    time_horizon = st.number_input("Time Horizon (years)", value=1.0, step=0.1, format="%.2f",
                                   help="How long until options expire")
    
    run_simulation = st.button("Run Simulation", type="primary", use_container_width=True)

with main_col:
    if len(st.session_state.portfolio) > 0:
        if run_simulation:
            with st.spinner("Running Monte Carlo simulation..."):
                # Update portfolio parameters
                for asset in st.session_state.portfolio:
                    if hasattr(asset, 'spot'):
                        asset.spot = spot
                    if hasattr(asset, 'maturity'):
                        asset.maturity = time_horizon
                    if hasattr(asset, 'volatility'):
                        asset.volatility = volatility
                    if hasattr(asset, 'rfr'):
                        asset.rfr = rfr
                
                # Run simulation
                results = simulate_portfolio_pnl(
                    portfolio=st.session_state.portfolio,
                    spot=spot,
                    expected_drift=expected_drift,
                    volatility=volatility,
                    maturity=time_horizon,
                    rfr=rfr,
                    num_simulations=num_simulations
                )
                
                # Store results in session state
                st.session_state.pnl_results = results
        
        # Display results if they exist
        if 'pnl_results' in st.session_state:
            results = st.session_state.pnl_results
            
            st.subheader("Portfolio Statistics")
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Initial Cost", f"${results['initial_cost']:.2f}")
                st.metric("Mean PnL", f"${results['mean']:.2f}")
            with col2:
                st.metric("Std Dev", f"${results['std']:.2f}")
                st.metric("Min PnL", f"${results['min']:.2f}")
            with col3:
                st.metric("Skewness", f"{results['skew']:.3f}")
                st.metric("Max PnL", f"${results['max']:.2f}")
            with col4:
                st.metric("Kurtosis", f"{results['kurtosis']:.3f}")
                st.metric("5th %ile", f"${results['percentile_5']:.2f}")
            
            # Create histogram
            st.subheader("PnL Distribution")
            
            fig = go.Figure()
            
            fig.add_trace(go.Histogram(
                x=results['pnl_samples'],
                nbinsx=50,
                name='PnL Distribution',
                marker=dict(
                    color='#ff4b4b',
                    line=dict(color='white', width=1)
                ),
                hovertemplate='PnL: %{x:.2f}<br>Count: %{y}<extra></extra>'
            ))
            
            # Add vertical line at mean
            fig.add_vline(
                x=results['mean'], 
                line_dash="dash", 
                line_color="yellow",
                annotation_text=f"Mean: ${results['mean']:.2f}",
                annotation_position="top"
            )
            
            # Add vertical line at zero
            fig.add_vline(
                x=0, 
                line_dash="dot", 
                line_color="white",
                opacity=0.5
            )
            
            fig.update_layout(
                title="Probability Distribution of Profit and Loss",
                xaxis_title="Profit/Loss ($)",
                yaxis_title="Frequency",
                height=500,
                plot_bgcolor='#0e1117',
                paper_bgcolor='#0e1117',
                font=dict(color='white'),
                showlegend=False,
                hovermode='x'
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Probability metrics
            st.subheader("Probability Analysis")
            prob_profit = np.mean(results['pnl_samples'] > 0) * 100
            prob_loss = np.mean(results['pnl_samples'] < 0) * 100
            prob_total_loss = np.mean(results['pnl_samples'] <= -results['initial_cost']) * 100
            
            col1, col2, col3 = st.columns(3)
            col1.metric("Probability of Profit", f"{prob_profit:.1f}%")
            col2.metric("Probability of Loss", f"{prob_loss:.1f}%")
            col3.metric("Prob. of Total Loss", f"{prob_total_loss:.1f}%")
            
            # Educational insights
            with st.expander("📚 Understanding These Results"):
                st.markdown(f"""
                **What does this tell us?**
                
                Your portfolio has an initial cost of **${results['initial_cost']:.2f}**. After running 
                {num_simulations:,} simulations of possible future scenarios, here's what we learned:
                
                - **Average Outcome**: The mean PnL is ${results['mean']:.2f}. However, notice that the 
                  average doesn't tell the whole story with options!
                
                - **Risk (Standard Deviation)**: The outcomes vary by ${results['std']:.2f}. This measures 
                  how uncertain your results are. Higher = more risk.
                
                - **Skewness ({results['skew']:.2f})**: {"Positive skew means you have a chance of very large gains, but most outcomes are smaller losses." if results['skew'] > 0 else "Negative skew means you have a chance of very large losses, but most outcomes are smaller gains."}
                
                - **Probability of Profit**: There's a {prob_profit:.1f}% chance you'll make money. 
                  This is often more useful than the average!
                
                **Why does expected drift matter?** 
                
                If you believe the stock will grow faster than {expected_drift*100:.0f}% per year, 
                calls become more attractive. If you think it will grow slower, puts look better. 
                The Black-Scholes price uses the risk-free rate, but YOUR outcomes depend on what actually happens!
                """)
        
        else:
            st.info("Click 'Run Simulation' to generate the PnL distribution")
            
    else:
        st.info("📊 No portfolio loaded. Add assets on the Portfolio Input page to see their PnL distribution.")