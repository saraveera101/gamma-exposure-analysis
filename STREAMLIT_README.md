# 🔥 Gamma Exposure Dashboard

A comprehensive Streamlit web application for analyzing options gamma exposure using the HeatSeeker methodology.

## Features

- **Interactive Gamma Matrix Heatmap**: Visual representation of gamma exposure by strike and expiration
- **Key Levels Analysis**: Identification of important support/resistance levels based on gamma
- **Real-time Data**: Live options data from yfinance
- **Multiple Display Formats**: Dataframes, charts, and downloadable CSV exports
- **Popular Tickers**: Quick access to commonly traded symbols (SPY, QQQ, AAPL, TSLA, etc.)

## Quick Start

### Option 1: Simple Launch (Recommended)
```bash
python launch_streamlit.py
```

### Option 2: Direct Streamlit Command
```bash
# Install requirements (first time only)
pip install -r requirements_streamlit.txt

# Run the dashboard
streamlit run streamlit_app.py
```

## How to Use

1. **Start the Application**: Use one of the launch methods above
2. **Enter Ticker Symbol**: Type any stock symbol in the sidebar (e.g., SPY, AAPL, TSLA)
3. **Click Analyze**: Press the "🚀 Analyze Gamma Exposure" button
4. **Explore Results**: 
   - **Gamma Matrix Tab**: Interactive heatmap and filterable data table
   - **Key Levels Tab**: Important support/resistance levels for trading
   - **Gamma Profile Tab**: Bar chart showing gamma exposure by strike
   - **Analysis Summary Tab**: Market regime and trading implications

## Dashboard Tabs

### 📊 Gamma Matrix
- **Interactive Heatmap**: Visual gamma exposure with current price overlay
- **Data Table**: Filterable matrix with price range controls
- **Download**: Export full matrix as CSV

### 🎯 Key Levels
- **Support/Resistance**: Nearest significant gamma levels
- **Trading Levels**: Important strikes for decision making
- **Distance Analysis**: Percentage distance from current price

### 📈 Gamma Profile
- **Strike Analysis**: Bar chart of gamma exposure by strike price
- **King Node Highlighting**: Largest gamma exposure levels
- **Summary Statistics**: Total positive/negative gamma breakdown

### 📋 Analysis Summary
- **Market Regime**: Positive/negative gamma environment
- **Trading Implications**: Expected volatility and price behavior
- **Dealer Positioning**: Call/put gamma analysis

## Key Concepts

### Market Regimes
- **🟡 Positive Gamma**: Lower volatility, mean-reverting behavior
- **🟣 Negative Gamma**: Higher volatility, trending behavior
- **⚪ Mixed Gamma**: Moderate volatility, mixed signals

### HeatSeeker Methodology
- **King Node**: Largest absolute gamma exposure level
- **Gamma Walls**: Significant support/resistance from options positioning
- **Dealer Flow**: How market makers may react to price movements

## Popular Symbols

The dashboard includes quick-access buttons for:
- **SPY**: S&P 500 ETF
- **QQQ**: Nasdaq 100 ETF  
- **AAPL**: Apple Inc.
- **TSLA**: Tesla Inc.
- **NVDA**: NVIDIA Corp.
- **NFLX**: Netflix Inc.

## Technical Requirements

- Python 3.8+
- Internet connection (for live options data)
- Modern web browser

## Dependencies

All required packages are listed in `requirements_streamlit.txt`:
- streamlit
- plotly
- pandas
- numpy
- yfinance
- scipy
- matplotlib
- seaborn

## Troubleshooting

### Common Issues

1. **"No options data available"**
   - Check if the ticker symbol is valid
   - Ensure market is open or try during market hours
   - Some stocks may have limited options activity

2. **Slow loading**
   - Options data download can take 10-30 seconds
   - Progress bar shows current status
   - Larger option chains (like SPY) take longer

3. **Empty gamma matrix**
   - Try adjusting the price range filter
   - Check if options have sufficient volume
   - Some tickers may have sparse options data

### Browser Access

Once running, the dashboard is available at:
- **Local**: http://localhost:8501
- **Network**: Available to other devices on your network

## File Structure

```
gamma_exposure/
├── streamlit_app.py           # Main Streamlit application
├── launch_streamlit.py        # Simple launcher script
├── requirements_streamlit.txt # Streamlit-specific requirements
├── gamma_exposure_analyzer.py # Core analysis engine
├── advanced_analysis.py       # Advanced gamma calculations
└── csv_exporter.py           # CSV export functionality
```

## Usage Tips

1. **Start with Popular Symbols**: Use SPY or QQQ to see typical gamma patterns
2. **Monitor During Market Hours**: Best data quality when markets are open
3. **Use Price Range Filter**: Focus on relevant strikes near current price
4. **Download Data**: Export CSV files for further analysis
5. **Watch King Nodes**: These are critical levels for price action

## Educational Purpose

This tool is for educational and analytical purposes only. It is not financial advice and should not be used as the sole basis for trading decisions.

---

**🔥 Happy Trading!** 

*Built with the HeatSeeker methodology for options gamma exposure analysis*