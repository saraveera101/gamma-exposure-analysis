# Quick Start Guide

## 🚀 Getting Started with Gamma Exposure Analysis

### Installation

1. **Clone the repository:**
```bash
git clone https://github.com/saraveera101/gamma-exposure-analysis.git
cd gamma-exposure-analysis
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Run the application:**
```bash
streamlit run app.py
```

The dashboard will automatically open in your browser at `http://localhost:8501`

### Using the Dashboard

#### Step 1: Configure Analysis
In the sidebar, you'll find:
- **Ticker Symbol**: Enter any stock symbol (e.g., SPY, AAPL, TSLA)
- **Risk-Free Rate**: Adjust the risk-free rate (default: 5%)
- **Number of Expirations**: Select how many expiration dates to analyze (1-10)
- **Use Demo Data**: Check this to use sample data for demonstration

#### Step 2: Run Analysis
Click the "🔍 Analyze Gamma Exposure" button to start the analysis.

#### Step 3: Interpret Results
The dashboard will display:
- **Key Metrics**: Current price, zero gamma level, total open interest, total GEX
- **Gamma Exposure Chart**: Bar chart showing gamma exposure by strike
- **Gamma Profile**: Calls vs puts comparison
- **Open Interest Distribution**: Where the volume is concentrated
- **Detailed Data Tables**: Raw options data and aggregated gamma exposure

### Understanding the Charts

**Gamma Exposure Bar Chart:**
- Green bars = Positive gamma exposure (market stabilizing)
- Red bars = Negative gamma exposure (market amplifying)
- Blue dashed line = Current price
- Orange dotted line = Zero gamma level

**Key Levels:**
- **Zero Gamma Level**: Critical price where gamma exposure changes sign
- **Max Positive GEX**: Strongest support/resistance level
- **Max Negative GEX**: Potential acceleration point

### Tips

1. **Demo Mode**: If you don't have internet access or Yahoo Finance is unavailable, use "Demo Data" mode
2. **Popular Tickers**: Start with SPY, QQQ, or AAPL to see typical gamma exposure patterns
3. **Multiple Expirations**: Include 3-5 expirations for comprehensive analysis
4. **Compare Over Time**: Run analysis regularly to track how gamma levels shift

### Troubleshooting

**Issue**: "Unable to fetch data for [ticker]"
- **Solution**: Check the "Use Demo Data" box to use sample data

**Issue**: Charts not loading
- **Solution**: Refresh the page and try again

**Issue**: Python dependencies error
- **Solution**: Make sure you're using Python 3.8 or higher

### Example Analysis Workflow

1. Enter "SPY" as ticker
2. Keep default settings (5% risk-free rate, 3 expirations)
3. Check "Use Demo Data" for quick demonstration
4. Click "Analyze Gamma Exposure"
5. Review the zero gamma level - this is where the market tends to gravitate
6. Look at the max positive GEX strikes - these are strong support/resistance levels
7. Expand "View Detailed Data" to see the raw numbers

### Educational Resources

The dashboard includes:
- **About Gamma Exposure**: Explains what GEX is and why it matters
- **Interpretation Guide**: Detailed guide on reading the charts and metrics
- **Trading Implications**: How to use this information in your analysis

### Need Help?

- Check the built-in help tooltips (ⓘ icons)
- Read the full README.md for detailed documentation
- Review the interpretation guide in the dashboard

---

**Happy analyzing!** 🔥
