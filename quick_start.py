#!/usr/bin/env python3
"""
Quick Start Script for Gamma Exposure Analysis Tool
Run this script to get started immediately with gamma exposure analysis
"""

def install_requirements():
    """Install required packages"""
    import subprocess
    import sys
    
    print("📦 Installing required packages...")
    
    packages = [
        'yfinance>=0.2.28',
        'pandas>=2.0.0', 
        'numpy>=1.24.0',
        'scipy>=1.10.0',
        'matplotlib>=3.7.0',
        'seaborn>=0.12.0'
    ]
    
    for package in packages:
        try:
            print(f"   Installing {package}...")
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])
        except subprocess.CalledProcessError:
            print(f"   ⚠️ Failed to install {package}")
    
    # Optional packages
    optional_packages = ['plotly>=5.15.0', 'jupyter>=1.0.0']
    print("\n📦 Installing optional packages (for enhanced features)...")
    
    for package in optional_packages:
        try:
            print(f"   Installing {package}...")
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])
        except subprocess.CalledProcessError:
            print(f"   ⚠️ Failed to install {package} (optional)")

def quick_start_demo():
    """Run a quick start demonstration"""
    print("🚀 Quick Start Demo")
    print("=" * 40)
    
    try:
        from gamma_exposure_analyzer import GammaExposureAnalyzer
        
        # Demo with SPY
        print("📊 Analyzing SPY (S&P 500 ETF)...")
        analyzer = GammaExposureAnalyzer("SPY")
        
        # Get current price
        print("1️⃣ Getting current price...")
        current_price = analyzer.get_current_price()
        print(f"   Current SPY Price: ${current_price:.2f}")
        
        # Get options (limited for demo)
        print("\n2️⃣ Fetching options data...")
        print("   (This may take 30-60 seconds for SPY...)")
        options_data = analyzer.get_options_data()
        
        if options_data:
            total_options = sum(len(df) for df in options_data.values())
            print(f"   ✅ Found {len(options_data)} expiration dates")
            print(f"   ✅ Total options contracts: {total_options:,}")
        
        # Calculate gamma exposure
        print("\n3️⃣ Calculating gamma exposure...")
        gamma_data = analyzer.calculate_gamma_exposure()
        
        if gamma_data is not None:
            print(f"   ✅ Processed {len(gamma_data)} options")
            
            # Quick analysis
            sentiment = analyzer.analyze_market_sentiment()
            if sentiment:
                print(f"\n4️⃣ Market Analysis:")
                print(f"   📈 Market Regime: {sentiment['regime']}")
                print(f"   💰 Net Gamma Exposure: ${sentiment['net_gamma']:,.0f}")
                
                # Get key levels
                levels = analyzer.identify_gamma_levels()
                if levels and levels['king_node'] is not None:
                    king_strike = levels['king_node']['strike']
                    king_gamma = levels['king_node']['gamma_exposure']
                    print(f"   👑 King Node: ${king_strike:.0f} (${king_gamma:,.0f} exposure)")
                
                # Generate signals
                signals = analyzer.generate_trading_signals()
                if signals:
                    print(f"\n5️⃣ Trading Signals:")
                    for signal in signals[:3]:  # Show first 3 signals
                        print(f"   {signal}")
                
                print(f"\n6️⃣ Creating charts...")
                print("   📊 Gamma Profile Chart")
                analyzer.plot_gamma_profile()
                
                print("   🔥 Gamma Heatmap")
                analyzer.plot_gamma_exposure_heatmap()
                
                print(f"\n✅ Quick Start Demo Completed!")
                print(f"💡 SPY shows {sentiment['regime'].split('-')[0].strip()} environment")
                
            else:
                print("   ⚠️ Could not analyze market sentiment")
        else:
            print("   ⚠️ Could not calculate gamma exposure")
            
    except Exception as e:
        print(f"❌ Demo failed: {e}")
        print("\n🔧 Troubleshooting:")
        print("   1. Check internet connection")
        print("   2. Try during market hours")
        print("   3. Run: python test_setup.py")

def interactive_menu():
    """Interactive menu for different analysis options"""
    print("\n🎯 What would you like to analyze?")
    print("1. 📊 SPY (S&P 500 ETF)")
    print("2. 📱 QQQ (NASDAQ ETF)")  
    print("3. 🍎 AAPL (Apple)")
    print("4. ⚡ TSLA (Tesla)")
    print("5. 🎮 Custom Symbol")
    print("6. 🔍 Market Scanner")
    print("7. 📚 Educational Example")
    print("8. 📄 Export to CSV")
    print("9. ❌ Exit")
    
    while True:
        try:
            choice = input("\nEnter choice (1-9): ").strip()
            
            if choice == "1":
                analyze_symbol("SPY")
            elif choice == "2":
                analyze_symbol("QQQ")
            elif choice == "3":
                analyze_symbol("AAPL")
            elif choice == "4":
                analyze_symbol("TSLA")
            elif choice == "5":
                symbol = input("Enter symbol: ").strip().upper()
                if symbol:
                    analyze_symbol(symbol)
            elif choice == "6":
                run_market_scanner()
            elif choice == "7":
                educational_example()
            elif choice == "8":
                export_to_csv()
            elif choice == "9":
                print("👋 Thanks for using Gamma Exposure Analysis!")
                break
            else:
                print("❌ Invalid choice")
                
        except KeyboardInterrupt:
            print("\n👋 Thanks for using Gamma Exposure Analysis!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")

def analyze_symbol(symbol):
    """Analyze a specific symbol"""
    print(f"\n🔍 Analyzing {symbol}...")
    
    try:
        from gamma_exposure_analyzer import GammaExposureAnalyzer
        
        analyzer = GammaExposureAnalyzer(symbol)
        results = analyzer.run_complete_analysis()
        
        if results:
            print(f"✅ Analysis completed for {symbol}")
        else:
            print(f"❌ Analysis failed for {symbol}")
            
    except Exception as e:
        print(f"❌ Error analyzing {symbol}: {e}")

def run_market_scanner():
    """Run market scanner"""
    print("\n🔍 Running Market Scanner...")
    
    try:
        from advanced_analysis import create_gamma_scanner
        
        symbols = ["SPY", "QQQ", "IWM", "AAPL", "TSLA"]
        results = create_gamma_scanner(symbols)
        
        if results:
            print("\n📊 Scanner Results:")
            for symbol, data in results.items():
                regime = "🟡" if "Positive" in data['regime'] else "🟣" if "Negative" in data['regime'] else "⚪"
                print(f"   {regime} {symbol}: ${data['current_price']:.2f}")
                
    except Exception as e:
        print(f"❌ Scanner failed: {e}")

def export_to_csv():
    """Export gamma exposure data to CSV"""
    print("\n📄 Export Gamma Data to CSV")
    print("=" * 40)
    
    symbol = input("Enter symbol to export (e.g., SPY): ").strip().upper()
    if not symbol:
        symbol = "SPY"
    
    print("\n📁 Export Format:")
    print("1. 📊 All formats")
    print("2. 🔥 Gamma Matrix only")
    print("3. 📈 Gamma by Strike only")
    print("4. ⏰ Gamma by Expiration only")
    
    format_choice = input("Choose format (1-4): ").strip()
    format_map = {"1": "all", "2": "matrix", "3": "strike", "4": "expiration"}
    export_format = format_map.get(format_choice, "all")
    
    try:
        from csv_exporter import create_gamma_exports
        exported_files = create_gamma_exports(symbol, export_format)
        
        if exported_files:
            print(f"\n✅ CSV export completed!")
            print(f"📁 Check the export directory for your files")
        else:
            print(f"❌ CSV export failed")
            
    except Exception as e:
        print(f"❌ CSV export error: {e}")

def educational_example():
    """Run educational example"""
    print("\n📚 Educational Example")
    print("=" * 40)
    print("This example explains gamma exposure step by step...")
    
    try:
        from examples import educational_example as run_educational
        run_educational()
    except Exception as e:
        print(f"❌ Educational example failed: {e}")

def main():
    """Main function"""
    print("🔥 Gamma Exposure Analysis Tool - Quick Start")
    print("=" * 50)
    print("Based on HeatSeeker methodology for options flow analysis")
    print()
    
    # Check if basic imports work
    try:
        import yfinance
        import pandas
        import numpy
        import matplotlib
        print("✅ Core libraries detected")
    except ImportError as e:
        print(f"❌ Missing required library: {e}")
        print("\n📦 Installing requirements...")
        install_requirements()
        print("✅ Installation complete. Please restart the script.")
        return
    
    print("\n🎯 Choose your path:")
    print("1. 🚀 Quick Demo (SPY analysis)")
    print("2. 🎮 Interactive Menu")
    print("3. 🧪 Run Tests")
    print("4. 📖 View Documentation")
    
    try:
        choice = input("\nEnter choice (1-4): ").strip()
        
        if choice == "1":
            quick_start_demo()
        elif choice == "2":
            interactive_menu()
        elif choice == "3":
            import test_setup
            test_setup.main()
        elif choice == "4":
            print("\n📖 Documentation:")
            print("   📄 README.md - Complete documentation")
            print("   🎯 examples.py - Interactive examples")
            print("   🔧 test_setup.py - Test functionality")
            print("   🌐 GitHub: [Your repository URL here]")
        else:
            print("❌ Invalid choice")
            
    except KeyboardInterrupt:
        print("\n👋 Thanks for trying Gamma Exposure Analysis!")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()