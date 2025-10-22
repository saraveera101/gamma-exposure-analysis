# 🔥 Gamma Exposure Analysis Tool

A comprehensive Python toolkit for analyzing options gamma exposure using the HeatSeeker methodology. This project provides both command-line tools and an interactive Streamlit web dashboard for options traders and analysts.

## 🌟 Features

### Core Analysis Engine
- **Real-time Options Data**: Fetch live options data using yfinance
- **Gamma Exposure Calculation**: Calculate dealer gamma exposure using Black-Scholes Greeks
- **HeatSeeker Methodology**: Implement professional-grade gamma exposure analysis
- **Market Regime Detection**: Identify positive/negative gamma environments

### Streamlit Web Dashboard
- **Interactive Heatmaps**: Visual gamma exposure matrix with highlighting
- **Key Levels Analysis**: Identify important support/resistance levels
- **Customizable Time Horizons**: Filter expirations from 1-12 months
- **Real-time Updates**: Live data fetching and analysis
- **CSV Export**: Download analysis results in multiple formats

### Command-Line Tools
- **Batch Processing**: Analyze multiple symbols programmatically
- **CSV Export System**: 6 different export formats for various use cases
- **Advanced Analysis**: Dealer positioning and market sentiment analysis

## 🚀 Quick Start

### Installation

1. **Clone the repository**:
```bash
git clone https://github.com/yourusername/gamma_exposure.git
cd gamma_exposure
```

2. **Install dependencies**:
```bash
pip install -r requirements.txt
```

3. **Run the Streamlit dashboard**:
```bash
python launch_streamlit.py
```

Or directly:
```bash
streamlit run streamlit_app.py
```

### Command Line Usage

```python
from gamma_exposure_analyzer import GammaExposureAnalyzer

# Analyze a symbol
analyzer = GammaExposureAnalyzer("SPY")
gamma_data = analyzer.calculate_gamma_exposure()
sentiment = analyzer.analyze_market_sentiment()

print(f"Net Gamma Exposure: ${sentiment['net_gamma']:,.0f}")
print(f"Market Regime: {sentiment['regime']}")
```

## 📊 Analysis Components

### 1. Gamma Exposure Matrix
- **Strikes vs Expirations**: 2D matrix showing gamma exposure
- **Color-coded Heatmap**: Visual representation of gamma levels
- **Cell Highlighting**: Highest/lowest gamma for each expiration
- **Time Filtering**: Focus on relevant time horizons

### 2. Key Levels Identification
- **King Nodes**: Largest absolute gamma exposure levels
- **Support/Resistance**: Price levels with significant gamma
- **Distance Analysis**: Percentage distance from current price
- **Trading Implications**: Market behavior expectations

### 3. Market Sentiment Analysis
- **Gamma Regime**: Positive/Negative/Mixed gamma environments
- **Dealer Positioning**: Call vs Put gamma exposure
- **ATM Analysis**: At-the-money gamma concentration
- **Volatility Expectations**: Implied market behavior

### 4. CSV Export System
- **Raw Data**: Complete options chain with Greeks
- **Gamma Matrix**: Strikes vs expirations pivot table
- **Strike Summary**: Aggregated gamma by strike price
- **Expiration Summary**: Aggregated gamma by expiration date
- **Key Levels**: Important support/resistance levels
- **Analysis Summary**: Market regime and statistics

## 🛠️ File Structure

```
gamma_exposure/
├── 📱 streamlit_app.py              # Interactive web dashboard
├── 🔧 gamma_exposure_analyzer.py    # Core analysis engine
├── 📈 advanced_analysis.py          # Advanced calculations
├── 📄 csv_exporter.py              # CSV export functionality
├── 🚀 launch_streamlit.py          # Easy launcher for dashboard
├── ⚙️ export_gamma_csv.py          # Command-line CSV export
├── 📋 quick_start.py               # Interactive menu system
├── 📝 requirements.txt             # Python dependencies
├── 📘 STREAMLIT_README.md          # Detailed dashboard guide
└── 🔍 examples.py                  # Usage examples
```

## 📈 Key Concepts

### HeatSeeker Methodology
- **Gamma Exposure**: How much underlying stock dealers must buy/sell per $1 move
- **King Nodes**: Strikes with largest absolute gamma exposure
- **Gamma Walls**: Significant support/resistance from options positioning
- **Dealer Flow**: Market maker hedging behavior and its price impact

### Market Regimes
- **🟡 Positive Gamma**: Lower volatility, mean-reverting behavior
- **🟣 Negative Gamma**: Higher volatility, trending behavior  
- **⚪ Mixed Gamma**: Transitional or balanced gamma environment

### Trading Applications
- **Intraday Levels**: Key support/resistance for day trading
- **Volatility Forecasting**: Expected price behavior based on gamma
- **Options Flow**: Understanding dealer positioning and flow
- **Risk Management**: Identifying high-impact price levels

## 🎯 Popular Use Cases

### For Day Traders
- Identify intraday support/resistance levels
- Understand volatility expectations
- Time entries around gamma levels

### For Options Traders
- Analyze dealer positioning
- Identify high-impact expiration dates
- Plan strategies around gamma walls

### For Analysts
- Research market structure
- Export data for further analysis
- Monitor institutional flow patterns

### For Educators
- Understand options market mechanics
- Visualize gamma exposure concepts
- Demonstrate dealer hedging effects

## 📊 Supported Symbols

Works with any optionable symbol including:
- **ETFs**: SPY, QQQ, IWM, XLF, etc.
- **Stocks**: AAPL, TSLA, NVDA, MSFT, etc.
- **Indices**: Options on index ETFs
- **International**: ETFs with US-listed options

## ⚙️ Technical Requirements

- **Python**: 3.8+ 
- **Memory**: 2GB+ RAM recommended
- **Internet**: Required for live data fetching
- **Browser**: Modern browser for Streamlit dashboard

## 📦 Dependencies

### Core Libraries
- `pandas` - Data manipulation and analysis
- `numpy` - Numerical computations
- `yfinance` - Yahoo Finance data API
- `scipy` - Statistical calculations

### Visualization
- `streamlit` - Web dashboard framework
- `plotly` - Interactive charts and heatmaps
- `matplotlib` - Static plotting
- `seaborn` - Statistical visualization

### Options Pricing
- `mibian` - Black-Scholes implementation (optional)
- Built-in Black-Scholes calculator included

## 🔧 Configuration

### Data Sources
- **Primary**: Yahoo Finance (yfinance)
- **Backup**: Built-in error handling for data issues
- **Rate Limiting**: Automatic retry logic for API limits

### Analysis Parameters
- **Time Horizon**: 1-12 months (default: 3 months)
- **Price Range**: 5-50% around current price (default: 25%)
- **Greeks Calculation**: Black-Scholes with automatic parameter detection

## 🚨 Important Notes

### Educational Purpose
This tool is for educational and analytical purposes only. It is not financial advice and should not be used as the sole basis for trading decisions.

### Data Accuracy
- Options data quality varies by symbol and time
- Best results during market hours
- Some symbols may have limited options activity

### Performance
- Large option chains (like SPY) may take 30-60 seconds to process
- Consider using smaller time horizons for faster results
- CSV exports are optimized for large datasets

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **HeatSeeker Methodology**: Professional options flow analysis techniques
- **Options Community**: For sharing knowledge and best practices
- **Open Source Libraries**: Pandas, NumPy, Streamlit, and others that make this possible

## 📞 Support

- **Issues**: Report bugs via GitHub Issues
- **Discussions**: Use GitHub Discussions for questions
- **Documentation**: Check STREAMLIT_README.md for dashboard details

---

**🔥 Happy Trading!**

*Built with ❤️ for the options trading community*