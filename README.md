# 🔥 Gamma Exposure Analysis Tool

Professional gamma exposure analysis tool with interactive Streamlit dashboard for options trading analysis.

## 📋 Overview

This tool provides comprehensive gamma exposure (GEX) analysis for stock options, helping traders identify key support/resistance levels and understand market maker positioning. Built with Python and Streamlit, it offers real-time data fetching, professional visualizations, and actionable insights.

## ✨ Features

- **Real-time Options Data**: Fetch live options chain data using Yahoo Finance
- **Gamma Exposure Calculation**: Black-Scholes based gamma calculations
- **Interactive Dashboard**: Professional Streamlit interface with multiple visualizations
- **Key Level Identification**: Automatically identifies zero gamma level and critical strikes
- **Calls vs Puts Analysis**: Separate gamma profiles for calls and puts
- **Open Interest Visualization**: Distribution of open interest across strikes
- **Interpretation Guide**: Built-in educational content explaining GEX concepts

## 🚀 Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Setup

1. Clone the repository:
```bash
git clone https://github.com/saraveera101/gamma-exposure-analysis.git
cd gamma-exposure-analysis
```

2. Install required dependencies:
```bash
pip install -r requirements.txt
```

## 💻 Usage

### Running the Dashboard

Start the Streamlit application:

```bash
streamlit run app.py
```

The dashboard will open in your default web browser at `http://localhost:8501`

### Using the Tool

1. **Enter Ticker**: Type a stock symbol (e.g., SPY, AAPL, TSLA) in the sidebar
2. **Configure Settings**:
   - Adjust risk-free rate (default: 5%)
   - Select number of expiration dates to analyze (1-10)
3. **Analyze**: Click "🔍 Analyze Gamma Exposure" button
4. **Explore Results**:
   - View key gamma levels and metrics
   - Analyze interactive charts
   - Review detailed data tables
   - Read interpretation guide

### Example Tickers

Try these popular tickers:
- **SPY**: S&P 500 ETF
- **QQQ**: Nasdaq 100 ETF  
- **AAPL**: Apple Inc.
- **TSLA**: Tesla Inc.
- **NVDA**: NVIDIA Corporation
- **IWM**: Russell 2000 ETF

## 📊 Understanding Gamma Exposure

### What is Gamma Exposure?

Gamma exposure (GEX) measures how much market makers need to hedge their positions as the underlying price changes:

- **Positive GEX**: Market makers sell into rallies and buy dips → **stabilizing** effect
- **Negative GEX**: Market makers buy rallies and sell dips → **amplifying** effect
- **Zero Gamma Level**: Critical price where GEX changes sign

### Key Metrics

- **Zero Gamma Level**: Price where net gamma exposure crosses zero
- **Max Positive GEX**: Strike with highest positive exposure (strong support/resistance)
- **Max Negative GEX**: Strike with most negative exposure (acceleration point)
- **Total GEX**: Overall market positioning (positive = stable, negative = volatile)

### Trading Implications

- **Above Zero Gamma**: Lower volatility expected
- **Below Zero Gamma**: Higher volatility expected
- **Large Positive GEX Strikes**: Strong support/resistance levels
- **Large Negative GEX**: Potential for rapid moves

## 🏗️ Project Structure

```
gamma-exposure-analysis/
├── app.py                      # Main Streamlit application
├── requirements.txt            # Python dependencies
├── README.md                   # This file
├── src/
│   ├── __init__.py
│   ├── gamma_calculator.py    # Gamma calculation engine
│   └── data_fetcher.py        # Options data fetching utilities
└── utils/
    ├── __init__.py
    └── visualizations.py      # Chart and visualization functions
```

## 🔧 Technical Details

### Gamma Calculation

The tool uses the Black-Scholes model to calculate gamma:

```
Gamma = N'(d1) / (S * σ * √T)
```

Where:
- N'(d1) = Standard normal probability density function
- S = Spot price
- σ = Implied volatility
- T = Time to expiration

### Gamma Exposure Formula

```
GEX = ±Gamma × Open Interest × Multiplier × Spot²
```

Market makers are:
- Short gamma for net call buying (negative sign)
- Long gamma for net put buying (positive sign)

## 📦 Dependencies

- **streamlit**: Interactive web dashboard
- **pandas**: Data manipulation
- **numpy**: Numerical computations
- **plotly**: Interactive visualizations
- **yfinance**: Options data fetching
- **scipy**: Statistical functions (Black-Scholes)

## ⚠️ Disclaimer

This tool is for **educational and informational purposes only**. It is not financial advice. Always conduct your own research and consult with qualified financial professionals before making investment decisions.

- Options trading carries significant risk
- Past performance doesn't guarantee future results
- Data accuracy depends on third-party sources
- The author is not responsible for trading losses

## 🤝 Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.

## 📝 License

This project is open source and available under the MIT License.

## 👤 Author

**Sara Veera**
- GitHub: [@saraveera101](https://github.com/saraveera101)

## 🙏 Acknowledgments

- Options data provided by Yahoo Finance via yfinance
- Built with Streamlit framework
- Inspired by professional gamma exposure analysis tools

---

**Made with ❤️ for the trading community**
