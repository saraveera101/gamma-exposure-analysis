"""
Streamlit Web Application for Gamma Exposure Analysis
Interactive dashboard for displaying gamma matrix and key levels
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import time
from datetime import datetime as dt, timedelta
import warnings

# Import our gamma exposure modules
from gamma_exposure_analyzer import GammaExposureAnalyzer
from advanced_analysis import AdvancedGammaAnalysis

warnings.filterwarnings('ignore')

# Configure Streamlit page
st.set_page_config(
    page_title="Gamma Exposure Dashboard",
    page_icon="🔥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main > div {
        padding-top: 2rem;
    }
    .stMetric {
        background-color: #f0f2f6;
        border: 1px solid #e0e0e0;
        padding: 10px;
        border-radius: 5px;
    }
    .gamma-positive {
        background-color: #d4edda;
        color: #155724;
        padding: 5px;
        border-radius: 3px;
    }
    .gamma-negative {
        background-color: #f8d7da;
        color: #721c24;
        padding: 5px;
        border-radius: 3px;
    }
</style>
""", unsafe_allow_html=True)

def create_gamma_heatmap(gamma_matrix, current_price, symbol, months_ahead=3):
    """Create an interactive heatmap of gamma exposure"""
    if gamma_matrix is None or gamma_matrix.empty:
        return None
    
    # Limit to strikes within reasonable range of current price
    price_range = current_price * 0.25  # 25% range
    relevant_strikes = gamma_matrix.index[
        (gamma_matrix.index >= current_price - price_range) &
        (gamma_matrix.index <= current_price + price_range)
    ]
    
    if len(relevant_strikes) == 0:
        relevant_strikes = gamma_matrix.index
    
    # Filter columns to only show expirations within specified months
    current_date = dt.now()
    months_out = current_date + timedelta(days=30 * months_ahead)
    
    # Filter columns by date (assuming column names are date strings)
    relevant_columns = []
    for col in gamma_matrix.columns:
        try:
            # Try to parse the column as a date
            col_date = dt.strptime(str(col), '%Y-%m-%d')
            if col_date <= months_out:
                relevant_columns.append(col)
        except (ValueError, TypeError):
            # If parsing fails, include the column (might be a different format)
            relevant_columns.append(col)
    
    # Limit to first 12 columns if we still have too many (for heatmap readability)
    if len(relevant_columns) > 12:
        relevant_columns = relevant_columns[:12]
    
    # Get subset of data
    plot_matrix = gamma_matrix.loc[relevant_strikes, relevant_columns]
    
    # Create heatmap
    fig = go.Figure(data=go.Heatmap(
        z=plot_matrix.values,
        x=plot_matrix.columns,
        y=plot_matrix.index,
        colorscale='RdYlBu_r',
        zmid=0,
        hovertemplate='Strike: $%{y}<br>Expiration: %{x}<br>Gamma Exposure: $%{z:,.0f}<extra></extra>',
        colorbar=dict(title="Gamma Exposure ($)")
    ))
    
    # Add current price line
    fig.add_hline(
        y=current_price,
        line_dash="dash",
        line_color="red",
        line_width=3,
        annotation_text=f"Current Price: ${current_price:.2f}",
        annotation_position="left"
    )
    
    fig.update_layout(
        title=f"{symbol} Gamma Exposure Heatmap",
        xaxis_title="Expiration Date",
        yaxis_title="Strike Price",
        height=600,
        xaxis=dict(tickangle=45)
    )
    
    return fig

def create_gamma_profile_chart(gamma_by_strike, current_price, symbol):
    """Create gamma exposure profile bar chart"""
    if gamma_by_strike is None or gamma_by_strike.empty:
        return None
    
    # Sort by strike
    gamma_by_strike = gamma_by_strike.sort_values('strike')
    
    # Create color mapping
    colors = ['green' if x > 0 else 'red' for x in gamma_by_strike['gamma_exposure']]
    
    fig = go.Figure()
    
    # Add gamma exposure bars
    fig.add_trace(go.Bar(
        x=gamma_by_strike['strike'],
        y=gamma_by_strike['gamma_exposure'],
        marker_color=colors,
        hovertemplate='Strike: $%{x}<br>Gamma Exposure: $%{y:,.0f}<extra></extra>',
        name='Gamma Exposure'
    ))
    
    # Highlight king node
    king_node = gamma_by_strike[gamma_by_strike['is_king_node']]
    if len(king_node) > 0:
        fig.add_trace(go.Bar(
            x=king_node['strike'],
            y=king_node['gamma_exposure'],
            marker_color='gold',
            hovertemplate='King Node<br>Strike: $%{x}<br>Gamma Exposure: $%{y:,.0f}<extra></extra>',
            name='King Node'
        ))
    
    # Add current price line
    fig.add_vline(
        x=current_price,
        line_dash="dash",
        line_color="black",
        line_width=2,
        annotation_text=f"Current Price: ${current_price:.2f}"
    )
    
    fig.update_layout(
        title=f"{symbol} Gamma Exposure Profile",
        xaxis_title="Strike Price",
        yaxis_title="Gamma Exposure ($)",
        height=500,
        showlegend=True
    )
    
    return fig

def format_currency(value):
    """Format currency values for display"""
    if abs(value) >= 1e9:
        return f"${value/1e9:.2f}B"
    elif abs(value) >= 1e6:
        return f"${value/1e6:.2f}M"
    elif abs(value) >= 1e3:
        return f"${value/1e3:.2f}K"
    else:
        return f"${value:.2f}"

def format_gamma_regime(regime):
    """Format gamma regime with appropriate emoji and color"""
    if "Positive" in regime:
        return "🟡 " + regime, "gamma-positive"
    elif "Negative" in regime:
        return "🟣 " + regime, "gamma-negative"
    else:
        return "⚪ " + regime, ""

def main():
    """Main Streamlit application"""
    
    # Header
    st.title("🔥 Gamma Exposure Dashboard")
    st.markdown("**Real-time options gamma exposure analysis based on HeatSeeker methodology**")
    
    # Sidebar for inputs
    st.sidebar.header("📊 Analysis Parameters")
    
    # Ticker input
    ticker = st.sidebar.text_input(
        "Enter Ticker Symbol",
        value="SPY",
        help="Enter a stock symbol (e.g., SPY, AAPL, TSLA)"
    ).upper().strip()
    
    # Analysis button
    analyze_button = st.sidebar.button("🚀 Analyze Gamma Exposure", type="primary")
    
    # Popular symbols quick select
    st.sidebar.markdown("### 📈 Popular Symbols")
    col1, col2 = st.sidebar.columns(2)
    
    with col1:
        if st.button("SPY", key="spy"):
            ticker = "SPY"
            analyze_button = True
        if st.button("AAPL", key="aapl"):
            ticker = "AAPL"
            analyze_button = True
        if st.button("TSLA", key="tsla"):
            ticker = "TSLA"
            analyze_button = True
    
    with col2:
        if st.button("QQQ", key="qqq"):
            ticker = "QQQ"
            analyze_button = True
        if st.button("NVDA", key="nvda"):
            ticker = "NVDA"
            analyze_button = True
        if st.button("NFLX", key="nflx"):
            ticker = "NFLX"
            analyze_button = True
    
    # Main content area
    if not ticker:
        st.info("👆 Enter a ticker symbol in the sidebar to begin analysis")
        return
    
    if analyze_button or 'last_ticker' not in st.session_state or st.session_state.last_ticker != ticker:
        
        # Store current ticker
        st.session_state.last_ticker = ticker
        
        # Progress tracking
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        try:
            # Step 1: Initialize analyzer
            status_text.text("🔄 Initializing analyzer...")
            progress_bar.progress(10)
            
            analyzer = GammaExposureAnalyzer(ticker)
            
            # Step 2: Get current price
            status_text.text("💰 Getting current price...")
            progress_bar.progress(20)
            
            current_price = analyzer.get_current_price()
            if current_price is None:
                st.error(f"❌ Could not fetch current price for {ticker}")
                return
            
            # Step 3: Fetch options data
            status_text.text("📊 Fetching options data...")
            progress_bar.progress(40)
            
            options_data = analyzer.get_options_data()
            if not options_data:
                st.error(f"❌ No options data available for {ticker}")
                return
            
            # Step 4: Calculate gamma exposure
            status_text.text("🧮 Calculating gamma exposure...")
            progress_bar.progress(70)
            
            gamma_data = analyzer.calculate_gamma_exposure()
            if gamma_data is None:
                st.error(f"❌ Could not calculate gamma exposure for {ticker}")
                return
            
            # Step 5: Generate analysis
            status_text.text("📈 Generating analysis...")
            progress_bar.progress(90)
            
            # Get all analysis components
            gamma_matrix = analyzer.aggregate_gamma_by_expiration()
            gamma_by_strike = analyzer.aggregate_gamma_by_strike()
            vanna_matrix = analyzer.aggregate_vanna_by_expiration()
            charm_matrix = analyzer.aggregate_charm_by_expiration()
            sentiment = analyzer.analyze_market_sentiment()
            levels = analyzer.identify_gamma_levels()
            
            # Advanced analysis
            advanced = AdvancedGammaAnalysis(analyzer)
            key_levels = advanced.calculate_gex_profile_levels(10)
            positioning = advanced.calculate_dealer_positioning()
            
            progress_bar.progress(100)
            status_text.text("✅ Analysis complete!")
            time.sleep(1)
            
            # Clear progress indicators
            progress_bar.empty()
            status_text.empty()
            
            # Store results in session state
            st.session_state.analysis_results = {
                'ticker': ticker,
                'current_price': current_price,
                'gamma_matrix': gamma_matrix,
                'vanna_matrix': vanna_matrix,
                'charm_matrix': charm_matrix,
                'gamma_by_strike': gamma_by_strike,
                'sentiment': sentiment,
                'levels': levels,
                'key_levels': key_levels,
                'positioning': positioning,
                'analyzer': analyzer,
                'timestamp': dt.now()
            }
            
        except Exception as e:
            st.error(f"❌ Analysis failed: {str(e)}")
            return
    
    # Display results if available
    if 'analysis_results' in st.session_state:
        results = st.session_state.analysis_results
        
        # Header with basic info
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                label="Symbol",
                value=results['ticker'],
                help="Stock symbol being analyzed"
            )
        
        with col2:
            st.metric(
                label="Current Price",
                value=f"${results['current_price']:.2f}",
                help="Current stock price"
            )
        
        with col3:
            if results['sentiment']:
                net_gamma = results['sentiment']['net_gamma']
                st.metric(
                    label="Net Gamma Exposure",
                    value=format_currency(net_gamma),
                    delta=f"{'Positive' if net_gamma > 0 else 'Negative'} Regime",
                    help="Total net gamma exposure across all options"
                )
        
        with col4:
            if results['levels'] and results['levels']['king_node'] is not None:
                king_strike = results['levels']['king_node']['strike']
                st.metric(
                    label="King Node",
                    value=f"${king_strike:.0f}",
                    delta=f"{abs(king_strike - results['current_price'])/results['current_price']*100:.1f}% away",
                    help="Largest absolute gamma exposure level"
                )
        
        # Market regime
        if results['sentiment']:
            regime_text, regime_class = format_gamma_regime(results['sentiment']['regime'])
            st.markdown(f"### Market Regime: <span class='{regime_class}'>{regime_text}</span>", unsafe_allow_html=True)
        
        # Tabs for different views
        tab1, tab2, tab3, tab4 = st.tabs(["📊 Gamma Matrix", "🎯 Key Levels", "📈 Gamma Profile", "📋 Analysis Summary"])
        
        with tab1:
            st.subheader("🔥 Gamma Exposure Matrix")
            st.markdown("*Strikes (rows) vs Expirations (columns) - Values in USD*")
            st.info("📅 **Note**: Use the 'Months Ahead' slider to customize the expiration time horizon for optimal readability")
            
            if results['gamma_matrix'] is not None and not results['gamma_matrix'].empty:
                # Filter options (moved before heatmap so months_ahead is available)
                st.markdown("#### ⚙️ Display Options")
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    price_range_pct = st.slider(
                        "Price Range (%)",
                        min_value=5,
                        max_value=50,
                        value=25,
                        help="Show strikes within this percentage of current price"
                    )
                
                with col2:
                    show_zeros = st.checkbox(
                        "Show Zero Values",
                        value=False,
                        help="Include rows/columns with zero gamma exposure"
                    )
                
                with col3:
                    highlight_only = st.checkbox(
                        "Show Only Key Levels",
                        value=False,
                        help="Display only strikes with highest/lowest gamma for each expiration"
                    )
                
                with col4:
                    months_ahead = st.slider(
                        "Months Ahead",
                        min_value=1,
                        max_value=12,
                        value=3,
                        help="Number of months of expirations to display"
                    )
                
                # Display data table with filtering
                st.markdown("#### 📋 Gamma Matrix Data Table")
                
                # Filter matrix for display
                price_range = results['current_price'] * (price_range_pct / 100)
                filtered_matrix = results['gamma_matrix'].loc[
                    (results['gamma_matrix'].index >= results['current_price'] - price_range) &
                    (results['gamma_matrix'].index <= results['current_price'] + price_range)
                ]
                
                # Filter columns to only show expirations within selected months
                current_date = dt.now()
                months_out = current_date + timedelta(days=30 * months_ahead)
                
                relevant_columns = []
                for col in filtered_matrix.columns:
                    try:
                        col_date = dt.strptime(str(col), '%Y-%m-%d')
                        if col_date <= months_out:
                            relevant_columns.append(col)
                    except (ValueError, TypeError):
                        relevant_columns.append(col)
                
                # Limit to first 15 columns if we still have too many (for display purposes)
                if len(relevant_columns) > 15:
                    relevant_columns = relevant_columns[:15]
                
                # Apply column filtering
                if relevant_columns:
                    filtered_matrix = filtered_matrix[relevant_columns]
                
                if not show_zeros:
                    # Remove rows and columns that are all zeros
                    filtered_matrix = filtered_matrix.loc[~(filtered_matrix == 0).all(axis=1)]
                    filtered_matrix = filtered_matrix.loc[:, ~(filtered_matrix == 0).all(axis=0)]
                
                # If "Show Only Key Levels" is selected, filter to show only high/low strikes
                if highlight_only:
                    key_strikes = set()
                    for col in filtered_matrix.columns:
                        col_data = filtered_matrix[col]
                        non_zero_data = col_data[col_data != 0]
                        
                        if len(non_zero_data) > 0:
                            max_val = non_zero_data.max()
                            min_val = non_zero_data.min()
                            
                            # Add strikes with max/min values
                            if max_val > 0:
                                max_strikes = col_data[col_data == max_val].index
                                key_strikes.update(max_strikes)
                            
                            if min_val < 0:
                                min_strikes = col_data[col_data == min_val].index
                                key_strikes.update(min_strikes)
                    
                    if key_strikes:
                        filtered_matrix = filtered_matrix.loc[list(key_strikes)]
                        filtered_matrix = filtered_matrix.sort_index(ascending=False)
                else:
                    # Sort all data from highest to lowest strike
                    filtered_matrix = filtered_matrix.sort_index(ascending=False)
                
                # Format for display with k notation for values >= 1000
                def format_gamma_values(value):
                    """Format gamma values: use 'k' for thousands, regular numbers for < 1000"""
                    if pd.isna(value) or value == 0:
                        return "0"
                    
                    abs_value = abs(value)
                    if abs_value >= 1000:
                        # Format as k (thousands)
                        formatted = f"{value/1000:.1f}k"
                        # Remove unnecessary .0
                        if formatted.endswith('.0k'):
                            formatted = formatted[:-3] + 'k'
                        return formatted
                    else:
                        # Format as regular integer
                        return str(int(round(value)))
                
                # Create highlighting function for high/low values and king nodes (works on numerical data)
                def highlight_high_low(df):
                    """
                    Highlight highest and lowest values in each column, plus king nodes in yellow
                    """
                    # Create empty styling dataframe
                    styles = pd.DataFrame('', index=df.index, columns=df.columns)
                    
                    # Get king node strike price if available
                    king_node_strike = None
                    if results['levels'] and results['levels']['king_node'] is not None:
                        king_node_strike = results['levels']['king_node']['strike']
                    
                    # For each column (expiration), find high/low values
                    for col in df.columns:
                        col_data = df[col]
                        # Only consider non-zero values for highlighting
                        non_zero_data = col_data[col_data != 0]
                        
                        if len(non_zero_data) > 0:
                            max_val = non_zero_data.max()
                            min_val = non_zero_data.min()
                            
                            # First, highlight king node strike in yellow (highest priority)
                            if king_node_strike is not None and king_node_strike in df.index:
                                king_mask = df.index == king_node_strike
                                styles.loc[king_mask, col] = 'background-color: #FFD700; font-weight: bold; color: #B8860B; border: 2px solid #DAA520;'
                            
                            # Then highlight maximum values (positive gamma - green background)
                            # Only apply if not already highlighted as king node
                            if max_val > 0:
                                max_mask = (col_data == max_val) & (col_data != 0)
                                if king_node_strike is not None:
                                    max_mask = max_mask & (df.index != king_node_strike)
                                styles.loc[max_mask, col] = 'background-color: #90EE90; font-weight: bold; color: #006400;'
                            
                            # Highlight minimum values (negative gamma - red background)
                            # Only apply if not already highlighted as king node  
                            if min_val < 0:
                                min_mask = (col_data == min_val) & (col_data != 0)
                                if king_node_strike is not None:
                                    min_mask = min_mask & (df.index != king_node_strike)
                                styles.loc[min_mask, col] = 'background-color: #FFB6C1; font-weight: bold; color: #8B0000;'
                    
                    return styles
                
                # Apply highlighting to numerical data first
                styled_matrix = filtered_matrix.style.apply(highlight_high_low, axis=None)
                
                # Then apply the k-notation formatting to the styled dataframe
                def format_gamma_values(value):
                    """Format gamma values: use 'k' for thousands, regular numbers for < 1000"""
                    if pd.isna(value) or value == 0:
                        return "0"
                    
                    abs_value = abs(value)
                    if abs_value >= 1000:
                        # Format as k (thousands)
                        formatted = f"{value/1000:.1f}k"
                        # Remove unnecessary .0
                        if formatted.endswith('.0k'):
                            formatted = formatted[:-3] + 'k'
                        return formatted
                    else:
                        # Format as regular integer
                        return str(int(round(value)))
                
                # Apply number formatting after styling
                styled_matrix = styled_matrix.format(format_gamma_values)
                
                # Add legend for highlighting
                st.markdown("""
                **📊 Color Legend:**
                - � **Yellow**: King Node (highest absolute gamma exposure strike price)
                - �🟢 **Green**: Highest positive gamma exposure for each expiration
                - 🔴 **Red**: Highest negative gamma exposure for each expiration
                - ⚪ **White**: Other gamma exposure values
                """)
                
                st.dataframe(
                    styled_matrix,
                    width='stretch',
                    height=400
                )
                
                # Download button
                csv = results['gamma_matrix'].to_csv()
                st.download_button(
                    label="📥 Download Full Matrix CSV",
                    data=csv,
                    file_name=f"{results['ticker']}_gamma_matrix_{dt.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv"
                )
                
                # Add some spacing between matrices
                st.markdown("---")
                
                # Vanna Matrix Data Table
                st.markdown("#### 📊 Vanna Matrix Data Table")
                st.markdown("*Vanna exposure by strikes (rows) vs expirations (columns) - Values in USD*")
                
                if results['vanna_matrix'] is not None and not results['vanna_matrix'].empty:
                    # Apply same filtering logic as gamma matrix
                    filtered_vanna_matrix = results['vanna_matrix'].loc[
                        (results['vanna_matrix'].index >= results['current_price'] - price_range) &
                        (results['vanna_matrix'].index <= results['current_price'] + price_range)
                    ]
                    
                    # Apply column filtering (same relevant_columns as gamma matrix)
                    if relevant_columns:
                        # Make sure columns exist in vanna matrix
                        available_vanna_columns = [col for col in relevant_columns if col in filtered_vanna_matrix.columns]
                        if available_vanna_columns:
                            filtered_vanna_matrix = filtered_vanna_matrix[available_vanna_columns]
                    
                    if not show_zeros:
                        # Remove rows and columns that are all zeros
                        filtered_vanna_matrix = filtered_vanna_matrix.loc[~(filtered_vanna_matrix == 0).all(axis=1)]
                        filtered_vanna_matrix = filtered_vanna_matrix.loc[:, ~(filtered_vanna_matrix == 0).all(axis=0)]
                    
                    # If "Show Only Key Levels" is selected, apply same filtering as gamma
                    if highlight_only:
                        if key_strikes:  # Use same key_strikes from gamma matrix
                            available_strikes = [s for s in key_strikes if s in filtered_vanna_matrix.index]
                            if available_strikes:
                                filtered_vanna_matrix = filtered_vanna_matrix.loc[available_strikes]
                                filtered_vanna_matrix = filtered_vanna_matrix.sort_index(ascending=False)
                    else:
                        # Sort all data from highest to lowest strike
                        filtered_vanna_matrix = filtered_vanna_matrix.sort_index(ascending=False)
                    
                    if not filtered_vanna_matrix.empty:
                        # Apply same styling as gamma matrix
                        styled_vanna_matrix = filtered_vanna_matrix.style.apply(highlight_high_low, axis=None)
                        styled_vanna_matrix = styled_vanna_matrix.format(format_gamma_values)
                        
                        st.dataframe(
                            styled_vanna_matrix,
                            width='stretch',
                            height=400
                        )
                        
                        # Download button for vanna matrix
                        vanna_csv = results['vanna_matrix'].to_csv()
                        st.download_button(
                            label="📥 Download Vanna Matrix CSV",
                            data=vanna_csv,
                            file_name=f"{results['ticker']}_vanna_matrix_{dt.now().strftime('%Y%m%d_%H%M%S')}.csv",
                            mime="text/csv"
                        )
                    else:
                        st.info("No vanna exposure data to display with current filters. Try adjusting the price range or enabling 'Show Zero Values'.")
                        
                else:
                    st.warning("No vanna matrix data available")
                
                # Add some spacing
                st.markdown("---")
                
                # Charm Matrix Data Table
                st.markdown("#### ⏰ Charm Matrix Data Table")
                st.markdown("*Charm exposure by strikes (rows) vs expirations (columns) - Values in USD*")
                
                if results['charm_matrix'] is not None and not results['charm_matrix'].empty:
                    # Apply same filtering logic as gamma matrix
                    filtered_charm_matrix = results['charm_matrix'].loc[
                        (results['charm_matrix'].index >= results['current_price'] - price_range) &
                        (results['charm_matrix'].index <= results['current_price'] + price_range)
                    ]
                    
                    # Apply column filtering (same relevant_columns as gamma matrix)
                    if relevant_columns:
                        # Make sure columns exist in charm matrix
                        available_charm_columns = [col for col in relevant_columns if col in filtered_charm_matrix.columns]
                        if available_charm_columns:
                            filtered_charm_matrix = filtered_charm_matrix[available_charm_columns]
                    
                    if not show_zeros:
                        # Remove rows and columns that are all zeros
                        filtered_charm_matrix = filtered_charm_matrix.loc[~(filtered_charm_matrix == 0).all(axis=1)]
                        filtered_charm_matrix = filtered_charm_matrix.loc[:, ~(filtered_charm_matrix == 0).all(axis=0)]
                    
                    # If "Show Only Key Levels" is selected, apply same filtering as gamma
                    if highlight_only:
                        if key_strikes:  # Use same key_strikes from gamma matrix
                            available_strikes = [s for s in key_strikes if s in filtered_charm_matrix.index]
                            if available_strikes:
                                filtered_charm_matrix = filtered_charm_matrix.loc[available_strikes]
                                filtered_charm_matrix = filtered_charm_matrix.sort_index(ascending=False)
                    else:
                        # Sort all data from highest to lowest strike
                        filtered_charm_matrix = filtered_charm_matrix.sort_index(ascending=False)
                    
                    if not filtered_charm_matrix.empty:
                        # Apply same styling as gamma matrix
                        styled_charm_matrix = filtered_charm_matrix.style.apply(highlight_high_low, axis=None)
                        styled_charm_matrix = styled_charm_matrix.format(format_gamma_values)
                        
                        st.dataframe(
                            styled_charm_matrix,
                            width='stretch',
                            height=400
                        )
                        
                        # Download button for charm matrix
                        charm_csv = results['charm_matrix'].to_csv()
                        st.download_button(
                            label="📥 Download Charm Matrix CSV",
                            data=charm_csv,
                            file_name=f"{results['ticker']}_charm_matrix_{dt.now().strftime('%Y%m%d_%H%M%S')}.csv",
                            mime="text/csv"
                        )
                    else:
                        st.info("No charm exposure data to display with current filters. Try adjusting the price range or enabling 'Show Zero Values'.")
                        
                else:
                    st.warning("No charm matrix data available")
                
            else:
                st.warning("No gamma matrix data available")
        
        with tab2:
            st.subheader("🎯 Key Gamma Exposure Levels")
            st.markdown("*Most important levels for trading decisions*")
            
            if results['key_levels'] is not None and not results['key_levels'].empty:
                # Format key levels for display
                display_levels = results['key_levels'].copy()
                display_levels['gamma_exposure_formatted'] = display_levels['gamma_exposure'].apply(format_currency)
                display_levels['distance_pct_formatted'] = display_levels['distance_pct'].apply(lambda x: f"{x:.1f}%")
                display_levels['strike_formatted'] = display_levels['strike'].apply(lambda x: f"${x:.2f}")
                
                # Always use 'direction' column as we confirmed it exists
                display_columns = [
                    'level_type', 'strike_formatted', 'gamma_exposure_formatted', 
                    'distance_pct_formatted', 'direction'
                ]
                column_names = {
                    'level_type': 'Level Type',
                    'strike_formatted': 'Strike Price',
                    'gamma_exposure_formatted': 'Gamma Exposure',
                    'distance_pct_formatted': 'Distance from Current',
                    'direction': 'Direction'
                }
                
                display_df = display_levels[display_columns].rename(columns=column_names)
                
                st.dataframe(
                    display_df,
                    width='stretch',
                    hide_index=True,
                    height=400
                )
                
                # Highlight key insights
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("#### 📈 Nearest Resistance")
                    resistance_levels = display_levels[display_levels['direction'] == 'Above'].head(3)
                    if not resistance_levels.empty:
                        for _, level in resistance_levels.iterrows():
                            st.markdown(f"• **${level['strike']:.0f}** - {level['distance_pct']:.1f}% above")
                    else:
                        st.markdown("*No significant resistance levels found*")
                
                with col2:
                    st.markdown("#### 📉 Nearest Support")
                    support_levels = display_levels[display_levels['direction'] == 'Below'].head(3)
                    if not support_levels.empty:
                        for _, level in support_levels.iterrows():
                            st.markdown(f"• **${level['strike']:.0f}** - {level['distance_pct']:.1f}% below")
                    else:
                        st.markdown("*No significant support levels found*")
                
                # Download button
                csv = results['key_levels'].to_csv(index=False)
                st.download_button(
                    label="📥 Download Key Levels CSV",
                    data=csv,
                    file_name=f"{results['ticker']}_key_levels_{dt.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv"
                )
                
            else:
                st.warning("No key levels data available")
        
        with tab3:
            st.subheader("📈 Gamma Exposure Profile")
            st.markdown("*Gamma exposure by strike price*")
            
            if results['gamma_by_strike'] is not None:
                # Display interactive chart
                profile_fig = create_gamma_profile_chart(
                    results['gamma_by_strike'],
                    results['current_price'],
                    results['ticker']
                )
                if profile_fig:
                    st.plotly_chart(profile_fig, width='stretch')
                
                # Summary statistics
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    positive_gamma = results['gamma_by_strike'][results['gamma_by_strike']['gamma_exposure'] > 0]['gamma_exposure'].sum()
                    st.metric("Total Positive Gamma", format_currency(positive_gamma))
                
                with col2:
                    negative_gamma = results['gamma_by_strike'][results['gamma_by_strike']['gamma_exposure'] < 0]['gamma_exposure'].sum()
                    st.metric("Total Negative Gamma", format_currency(negative_gamma))
                
                with col3:
                    net_gamma = positive_gamma + negative_gamma
                    st.metric("Net Gamma", format_currency(net_gamma))
        
        with tab4:
            st.subheader("📋 Analysis Summary")
            
            # Market sentiment details
            if results['sentiment']:
                st.markdown("#### 🎯 Market Sentiment Analysis")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    sentiment_data = {
                        'Metric': [
                            'Market Regime',
                            'Net Gamma Exposure',
                            'Total Positive Gamma',
                            'Total Negative Gamma',
                            'Near Money Gamma'
                        ],
                        'Value': [
                            results['sentiment']['regime'],
                            format_currency(results['sentiment']['net_gamma']),
                            format_currency(results['sentiment']['total_positive_gamma']),
                            format_currency(results['sentiment']['total_negative_gamma']),
                            format_currency(results['sentiment']['near_money_gamma'])
                        ]
                    }
                    
                st.dataframe(
                    pd.DataFrame(sentiment_data),
                    hide_index=True,
                    width='stretch'
                )
                
                with col2:
                    st.markdown("#### 💡 Trading Implications")
                    
                    regime = results['sentiment']['regime']
                    if "Positive" in regime:
                        st.success("🟡 **Positive Gamma Environment**")
                        st.markdown("""
                        - Expect **lower volatility**
                        - Price moves will be **dampened**
                        - **Mean-reverting** behavior likely
                        - Dealers provide liquidity **against** moves
                        """)
                    elif "Negative" in regime:
                        st.error("🟣 **Negative Gamma Environment**")
                        st.markdown("""
                        - Expect **higher volatility**
                        - Price moves may be **amplified**
                        - **Trending** behavior possible
                        - Dealers may **accelerate** moves
                        """)
                    else:
                        st.info("⚪ **Mixed Gamma Environment**")
                        st.markdown("""
                        - **Moderate volatility** expected
                        - Mixed price behavior
                        - Monitor for regime changes
                        """)
                
                # Gamma Flip Points Analysis
                if 'gamma_flip_points' in results['sentiment'] and results['sentiment']['gamma_flip_points']:
                    st.markdown("#### ⚡ Gamma Flip Points Analysis")
                    
                    flip_points = results['sentiment']['gamma_flip_points']
                    current_price = results['current_price']
                    
                    # Count and basic stats
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric(
                            label="Total Flip Points",
                            value=len(flip_points)
                        )
                    
                    # Find nearest flip points above and below current price
                    below_current = [fp for fp in flip_points if fp['strike'] < current_price]
                    above_current = [fp for fp in flip_points if fp['strike'] > current_price]
                    
                    nearest_below = max(below_current, key=lambda x: x['strike']) if below_current else None
                    nearest_above = min(above_current, key=lambda x: x['strike']) if above_current else None
                    
                    with col2:
                        if nearest_below:
                            distance_below = (current_price - nearest_below['strike']) / current_price * 100
                            st.metric(
                                label="Nearest Support Flip",
                                value=f"${nearest_below['strike']:.0f}",
                                delta=f"-{distance_below:.1f}%"
                            )
                        else:
                            st.metric(label="Nearest Support Flip", value="None")
                    
                    with col3:
                        if nearest_above:
                            distance_above = (nearest_above['strike'] - current_price) / current_price * 100
                            st.metric(
                                label="Nearest Resistance Flip",
                                value=f"${nearest_above['strike']:.0f}",
                                delta=f"+{distance_above:.1f}%"
                            )
                        else:
                            st.metric(label="Nearest Resistance Flip", value="None")
                    
                    # Key flip points near current price
                    nearby_flips = [fp for fp in flip_points 
                                  if abs(fp['strike'] - current_price) / current_price <= 0.15]  # Within 15%
                    
                    if nearby_flips:
                        st.markdown("**🎯 Key Flip Points Near Current Price (±15%):**")
                        flip_df = pd.DataFrame([
                            {
                                'Strike Price': f"${fp['strike']:.0f}",
                                'Distance': f"{((fp['strike'] - current_price) / current_price * 100):+.1f}%",
                                'Position': 'Above' if fp['strike'] > current_price else 'Below'
                            }
                            for fp in sorted(nearby_flips, key=lambda x: abs(x['strike'] - current_price))[:10]
                        ])
                        st.dataframe(flip_df, hide_index=True, width='stretch')
                    
                    # Trading implications
                    st.markdown("**📊 Flip Points Trading Implications:**")
                    if len(flip_points) > 30:
                        st.warning("⚠️ **High Flip Point Density** - Complex gamma environment with many volatility shift zones")
                    elif len(flip_points) > 15:
                        st.info("📈 **Moderate Flip Point Activity** - Several key levels to monitor")
                    else:
                        st.success("✅ **Clean Gamma Structure** - Few but important flip points")
                    
                    st.markdown("""
                    - **Flip Points** = Price levels where gamma exposure changes sign
                    - **Support Flips** = Levels below current price where volatility behavior shifts
                    - **Resistance Flips** = Levels above current price with potential volatility changes
                    - **Near Price Flips** = Most relevant for short-term trading decisions
                    """)
            
            # Dealer positioning
            if results['positioning']:
                st.markdown("#### 🏦 Dealer Positioning")
                
                positioning_data = {
                    'Metric': [
                        'Call Gamma Exposure',
                        'Put Gamma Exposure',
                        'ATM Call Gamma',
                        'ATM Put Gamma',
                        'Put/Call Gamma Ratio'
                    ],
                    'Value': [
                        format_currency(results['positioning']['call_gamma_exposure']),
                        format_currency(results['positioning']['put_gamma_exposure']),
                        format_currency(results['positioning']['atm_call_gamma']),
                        format_currency(results['positioning']['atm_put_gamma']),
                        f"{results['positioning']['pc_ratio_gamma']:.2f}"
                    ]
                }
                
                st.dataframe(
                    pd.DataFrame(positioning_data),
                    hide_index=True,
                    width='stretch'
                )
            
            # Analysis timestamp
            st.markdown(f"*Analysis completed at: {results['timestamp'].strftime('%Y-%m-%d %H:%M:%S')}*")
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666;'>
        🔥 <strong>Gamma Exposure Dashboard</strong> | Based on HeatSeeker Methodology<br>
        <small>For educational purposes only. Not financial advice.</small>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()