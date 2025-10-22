"""
🔥 Professional Gamma Exposure Analysis Dashboard
A Streamlit application for analyzing options gamma exposure
"""

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
import sys
import os

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'utils'))

from src.gamma_calculator import GammaCalculator
from src.data_fetcher import OptionsDataFetcher
from utils.visualizations import (
    create_gamma_exposure_chart,
    create_gamma_profile_chart,
    create_open_interest_chart,
    create_metrics_summary
)

# Page configuration
st.set_page_config(
    page_title="Gamma Exposure Analysis",
    page_icon="🔥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for professional styling
st.markdown("""
    <style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .stButton>button {
        width: 100%;
        background-color: #1f77b4;
        color: white;
        font-weight: bold;
        border-radius: 5px;
        padding: 0.5rem 1rem;
        border: none;
    }
    .stButton>button:hover {
        background-color: #155a8a;
    }
    </style>
""", unsafe_allow_html=True)

# Header
st.markdown('<div class="main-header">🔥 Gamma Exposure Analysis</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Professional options gamma exposure analysis tool</div>', unsafe_allow_html=True)

# Sidebar configuration
with st.sidebar:
    st.header("⚙️ Configuration")
    
    # Ticker input
    ticker = st.text_input(
        "Ticker Symbol",
        value="SPY",
        help="Enter a stock ticker (e.g., SPY, AAPL, QQQ)"
    ).upper()
    
    # Risk-free rate
    risk_free_rate = st.slider(
        "Risk-Free Rate (%)",
        min_value=0.0,
        max_value=10.0,
        value=5.0,
        step=0.1,
        help="Annual risk-free interest rate"
    ) / 100
    
    # Number of expirations to analyze
    max_expirations = st.slider(
        "Number of Expirations",
        min_value=1,
        max_value=10,
        value=3,
        help="Number of expiration dates to include in analysis"
    )
    
    # Analysis button
    analyze_button = st.button("🔍 Analyze Gamma Exposure", use_container_width=True)
    
    st.divider()
    
    # Information section
    with st.expander("ℹ️ About Gamma Exposure"):
        st.markdown("""
        **Gamma Exposure (GEX)** measures market makers' hedging requirements.
        
        - **Positive GEX**: Market makers hedge by selling into rallies and buying dips (stabilizing)
        - **Negative GEX**: Market makers hedge by buying rallies and selling dips (amplifying moves)
        - **Zero Gamma Level**: Critical price level where gamma exposure changes sign
        
        This tool helps identify key support/resistance levels based on options positioning.
        """)

# Main content area
if 'data_loaded' not in st.session_state:
    st.session_state.data_loaded = False

if analyze_button or st.session_state.data_loaded:
    with st.spinner(f"Fetching options data for {ticker}..."):
        try:
            # Initialize data fetcher
            fetcher = OptionsDataFetcher(ticker)
            
            # Get current price
            current_price = fetcher.get_current_price()
            
            if current_price is None:
                st.error(f"❌ Unable to fetch data for {ticker}. Please check the ticker symbol.")
                st.session_state.data_loaded = False
                st.stop()
            
            # Get ticker info
            ticker_info = fetcher.get_ticker_info()
            
            # Fetch options chain
            options_df = fetcher.fetch_options_chain(max_expirations=max_expirations)
            
            if options_df.empty:
                st.error(f"❌ No options data available for {ticker}")
                st.session_state.data_loaded = False
                st.stop()
            
            # Calculate gamma exposure
            calculator = GammaCalculator(current_price, risk_free_rate)
            gamma_df = calculator.calculate_gamma_exposure(options_df)
            aggregated_df = calculator.aggregate_gamma_by_strike(gamma_df)
            key_levels = calculator.find_gamma_levels(aggregated_df)
            
            st.session_state.data_loaded = True
            
            # Display ticker information
            st.header(f"📈 {ticker_info['name']}")
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Current Price", f"${current_price:.2f}")
            
            with col2:
                if key_levels:
                    zero_gamma = key_levels['zero_gamma_level']
                    delta = ((current_price - zero_gamma) / zero_gamma * 100)
                    st.metric("Zero Gamma Level", f"${zero_gamma:.2f}", 
                             f"{delta:+.2f}%")
            
            with col3:
                total_oi = options_df['oi'].sum()
                st.metric("Total Open Interest", f"{total_oi:,.0f}")
            
            with col4:
                total_gex = key_levels.get('total_gamma_exposure', 0) if key_levels else 0
                st.metric("Total GEX", f"{total_gex:,.0f}")
            
            st.divider()
            
            # Key metrics summary
            if key_levels:
                st.markdown(create_metrics_summary(key_levels), unsafe_allow_html=True)
            
            st.divider()
            
            # Gamma exposure chart
            st.subheader("📊 Gamma Exposure by Strike")
            fig_gamma = create_gamma_exposure_chart(aggregated_df, current_price, ticker)
            st.plotly_chart(fig_gamma, use_container_width=True)
            
            # Two column layout for additional charts
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("📉 Gamma Profile: Calls vs Puts")
                fig_profile = create_gamma_profile_chart(gamma_df, current_price, ticker)
                st.plotly_chart(fig_profile, use_container_width=True)
            
            with col2:
                st.subheader("📊 Open Interest Distribution")
                fig_oi = create_open_interest_chart(options_df, current_price, ticker)
                st.plotly_chart(fig_oi, use_container_width=True)
            
            # Data table
            with st.expander("📋 View Detailed Data"):
                st.subheader("Aggregated Gamma Exposure by Strike")
                st.dataframe(
                    aggregated_df.style.format({
                        'strike': '${:.2f}',
                        'gamma_exposure': '{:,.0f}',
                        'open_interest': '{:,.0f}'
                    }),
                    use_container_width=True
                )
                
                st.subheader("Raw Options Data")
                st.dataframe(
                    options_df.head(50),
                    use_container_width=True
                )
            
            # Interpretation guide
            with st.expander("📚 Interpretation Guide"):
                st.markdown("""
                ### How to Interpret Gamma Exposure Charts
                
                1. **Green Bars (Positive GEX)**: Indicate strikes where market makers provide liquidity by selling into strength and buying weakness
                2. **Red Bars (Negative GEX)**: Indicate strikes where market makers amplify moves by buying strength and selling weakness
                3. **Current Price Line (Blue Dashed)**: Shows where the underlying is currently trading
                4. **Zero Gamma Level (Orange Dotted)**: Critical level - price tends to gravitate toward this level
                
                ### Trading Implications
                
                - **Above Zero Gamma**: Expect lower volatility, price compression
                - **Below Zero Gamma**: Expect higher volatility, larger price swings
                - **Large Positive GEX at Strike**: Strong support/resistance level
                - **Large Negative GEX**: Potential for accelerated moves through that level
                
                ### Key Metrics Explained
                
                - **Zero Gamma Level**: Price where net gamma exposure crosses zero
                - **Max Positive GEX**: Strike with highest positive gamma exposure (strongest support/resistance)
                - **Max Negative GEX**: Strike with most negative gamma exposure (potential acceleration point)
                - **Total GEX**: Overall market maker positioning (positive = stabilizing, negative = destabilizing)
                """)
            
        except Exception as e:
            st.error(f"❌ An error occurred: {str(e)}")
            st.session_state.data_loaded = False
            import traceback
            with st.expander("Error Details"):
                st.code(traceback.format_exc())

else:
    # Welcome screen
    st.info("👈 Enter a ticker symbol in the sidebar and click 'Analyze Gamma Exposure' to begin")
    
    st.markdown("""
    ### Welcome to the Gamma Exposure Analysis Tool! 🔥
    
    This professional dashboard helps you analyze options gamma exposure for any stock with active options trading.
    
    #### Features:
    - 📊 Real-time options data fetching
    - 🎯 Gamma exposure calculations using Black-Scholes model
    - 📈 Interactive visualizations
    - 🔍 Key support/resistance level identification
    - 📉 Calls vs Puts gamma profile analysis
    - 💡 Trading implications and interpretation guide
    
    #### Popular Tickers to Try:
    - **SPY**: S&P 500 ETF
    - **QQQ**: Nasdaq 100 ETF
    - **AAPL**: Apple Inc.
    - **TSLA**: Tesla Inc.
    - **NVDA**: NVIDIA Corporation
    
    Get started by entering a ticker in the sidebar! 👈
    """)
    
    # Add sample visualization placeholder
    st.image("https://via.placeholder.com/800x400/1f77b4/ffffff?text=Gamma+Exposure+Visualization", 
             caption="Example: Gamma Exposure Chart")

# Footer
st.divider()
st.markdown("""
    <div style='text-align: center; color: #666; padding: 1rem;'>
        <small>
        Built with Streamlit | Data provided by Yahoo Finance<br>
        ⚠️ For educational purposes only. Not financial advice.
        </small>
    </div>
""", unsafe_allow_html=True)
