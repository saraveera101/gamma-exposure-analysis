# 🎯 QUICK USAGE GUIDE

## 🚀 Getting Started

### 1. Install Dependencies
```bash
pip install yfinance pandas numpy scipy matplotlib seaborn
```

### 2. Basic Analysis
```python
from gamma_exposure_analyzer import GammaExposureAnalyzer

# Create analyzer
analyzer = GammaExposureAnalyzer("SPY")

# Run complete analysis
results = analyzer.run_complete_analysis()
```

### 3. Interactive Menu
```bash
python examples.py
```

## 📊 What You'll Get

### Market Regime Analysis
- 🟡 **Positive Gamma**: Lower volatility, controlled moves
- 🟣 **Negative Gamma**: Higher volatility, chaotic moves

### Key Levels
- 👑 **King Nodes**: Largest gamma exposure levels
- 📈 **Resistance**: Where price may face selling
- 📉 **Support**: Where price may find buying

### Trading Signals
- Real-time gamma exposure analysis
- Support/resistance identification
- Volatility regime detection
- Market maker positioning insights

## 🔧 File Structure
```
gamma_exposure/
├── gamma_exposure_analyzer.py  # Main analysis engine
├── advanced_analysis.py        # Advanced features
├── examples.py                 # Interactive examples
├── quick_start.py             # Getting started script
├── test_setup.py              # Test functionality
├── config.py                  # Configuration settings
├── requirements.txt           # Dependencies
└── README.md                  # Full documentation
```

## 🎮 Quick Commands

### Analyze SPY
```python
from gamma_exposure_analyzer import GammaExposureAnalyzer
analyzer = GammaExposureAnalyzer("SPY")
analyzer.run_complete_analysis()
```

### Scan Multiple Symbols
```python
from advanced_analysis import create_gamma_scanner
results = create_gamma_scanner(["SPY", "QQQ", "AAPL"])
```

### Educational Example
```python
python quick_start.py
# Choose option 1 for demo
```

## 💡 Key Concepts

### Gamma Exposure Formula
```
Dealer Gamma Exposure = Open Interest × Gamma × 100 × S² × 0.01
```

### Interpretation
- **Positive Gamma**: Dealers provide liquidity against moves
- **Negative Gamma**: Dealers may amplify price moves
- **King Node**: Largest absolute gamma exposure = biggest magnet

### Market Regimes
```
🟡 Positive + Low Vol = Controlled, range-bound
🟣 Negative + High Vol = Volatile, trending
⚪ Mixed = Moderate volatility
```

## 🚨 Important Notes

1. **Market Hours**: Best data during trading hours (9:30-16:00 EST)
2. **Liquid Options**: Works best with liquid underlyings (SPY, QQQ, AAPL)
3. **Real-time Data**: yfinance provides delayed data (15-20 min)
4. **Educational Use**: For learning and research, not financial advice

## 🆘 Troubleshooting

### No Options Data
- Check if symbol has active options
- Verify during market hours
- Try more liquid symbols (SPY, QQQ)

### Slow Performance
- Large option chains take time
- SPY analysis: 30-60 seconds
- Consider filtering expirations

### Import Errors
```bash
pip install -r requirements.txt
python test_setup.py
```

### Empty CSV Matrix
- ✅ **Fixed in latest version** - Matrix now properly exports strikes vs expirations
- Ensure you have the latest code with the reindex fix
- If still empty, check if options have valid open interest and IV data

## 🎯 Next Steps

1. **Start with SPY**: Most liquid options market
2. **Learn the Concepts**: Understand gamma vs volatility
3. **Compare Symbols**: See how different stocks behave
4. **Paper Trading**: Test signals before real money
5. **Advanced Features**: Try multi-symbol scanning

## 📈 Example Output
```
Starting Gamma Exposure Analysis for SPY
==================================================
✅ Current Price: $428.50
✅ Fetched options for 43 expiration dates
✅ Calculated gamma exposure for 2,847 options
✅ Market Regime: Positive Gamma Environment - Expect Lower Volatility

Trading Signals:
📈 Resistance at $430 (0.4% above)
📉 Support at $425 (0.8% below)  
👑 King Node (Positive): $428 - Strong support/resistance level
🟡 Positive Gamma Environment - Expect Lower Volatility
==================================================
```

Happy Trading! 🚀📊