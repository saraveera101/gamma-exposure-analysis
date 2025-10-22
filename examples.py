"""
Example Usage and Testing Script for Gamma Exposure Analysis
"""

from gamma_exposure_analyzer import GammaExposureAnalyzer
from advanced_analysis import AdvancedGammaAnalysis, create_gamma_scanner
import pandas as pd
import matplotlib.pyplot as plt

def test_single_symbol(symbol="SPY"):
    """
    Test the gamma exposure analysis on a single symbol
    """
    print(f"Testing Gamma Exposure Analysis for {symbol}")
    print("=" * 60)
    
    try:
        # Create analyzer
        analyzer = GammaExposureAnalyzer(symbol)
        
        # Run complete analysis
        results = analyzer.run_complete_analysis()
        
        if results:
            print(f"\n✅ Analysis completed successfully for {symbol}")
            
            # Create advanced analysis
            advanced = AdvancedGammaAnalysis(analyzer)
            
            # Generate intraday levels report
            print("\n📊 Generating Advanced Analysis...")
            report = advanced.generate_intraday_levels_report()
            
            if report:
                print(f"✅ Intraday Levels Report Generated")
                print(f"   Market Regime: {report['market_regime']}")
                print(f"   Current Price: ${report['current_price']:.2f}")
                
                if 'key_levels' in report and report['key_levels'] is not None:
                    print(f"   Key Levels Found: {len(report['key_levels'])}")
                    
                    # Show top 3 levels
                    top_levels = report['key_levels'].head(3)
                    for _, level in top_levels.iterrows():
                        print(f"   - ${level['strike']:.0f}: {level['level_type']} "
                              f"({level['distance_pct']:.1f}% {level['direction']})")
            
            # Create comprehensive analysis chart
            print("\n📈 Creating Comprehensive Analysis Chart...")
            advanced.plot_comprehensive_analysis()
            
            return results, report
            
        else:
            print(f"❌ Analysis failed for {symbol}")
            return None, None
            
    except Exception as e:
        print(f"❌ Error analyzing {symbol}: {e}")
        return None, None

def test_multiple_symbols():
    """
    Test gamma exposure analysis on multiple symbols
    """
    symbols = ["SPY", "QQQ", "AAPL", "TSLA", "NVDA"]
    
    print("Testing Multiple Symbol Analysis")
    print("=" * 60)
    
    results = create_gamma_scanner(symbols)
    
    if results:
        print("\n✅ Multi-symbol analysis completed")
        
        # Create summary DataFrame
        summary_data = []
        for symbol, data in results.items():
            summary_data.append({
                'Symbol': symbol,
                'Current Price': f"${data['current_price']:.2f}",
                'Market Regime': data['regime'],
                'Net Gamma': f"${data['net_gamma']:,.0f}",
                'King Node': f"${data['king_node']:.0f}" if data['king_node'] else "N/A"
            })
        
        summary_df = pd.DataFrame(summary_data)
        print("\n📊 Summary Results:")
        print(summary_df.to_string(index=False))
        
        return results
    else:
        print("❌ Multi-symbol analysis failed")
        return None

def demo_advanced_features(symbol="SPY"):
    """
    Demonstrate advanced features of the gamma exposure analyzer
    """
    print(f"Advanced Features Demo for {symbol}")
    print("=" * 60)
    
    try:
        # Create analyzer and run basic analysis
        analyzer = GammaExposureAnalyzer(symbol)
        analyzer.get_current_price()
        analyzer.get_options_data()
        analyzer.calculate_gamma_exposure()
        
        # Create advanced analysis
        advanced = AdvancedGammaAnalysis(analyzer)
        
        print("1. 📊 Key GEX Profile Levels")
        levels = advanced.calculate_gex_profile_levels(5)
        if levels is not None:
            print(levels[['strike', 'gamma_exposure', 'level_type', 'distance_pct', 'direction']].to_string())
        
        print("\n2. 🏦 Dealer Positioning Analysis")
        positioning = advanced.calculate_dealer_positioning()
        if positioning:
            print(f"   Call Gamma Exposure: ${positioning['call_gamma_exposure']:,.0f}")
            print(f"   Put Gamma Exposure: ${positioning['put_gamma_exposure']:,.0f}")
            print(f"   Net Gamma Exposure: ${positioning['net_gamma_exposure']:,.0f}")
            print(f"   P/C Ratio (Gamma): {positioning['pc_ratio_gamma']:.2f}")
        
        print("\n3. 🎯 Dealer Hedging Zones")
        zones = advanced.identify_dealer_hedging_zones()
        if zones is not None:
            high_intensity = zones[zones['intensity'] == 'High'].head(3)
            print(high_intensity[['strike', 'zone_type', 'intensity', 'distance_pct']].to_string())
        
        print("\n4. 📈 Gamma Flip Scenarios")
        scenarios = advanced.calculate_gamma_flip_scenarios()
        if scenarios is not None:
            print(scenarios.to_string())
        
        print("\n5. ⏰ Expiration Impact Analysis")
        exp_impact = advanced.analyze_expiration_impact()
        if exp_impact is not None:
            print(exp_impact[['expiration', 'days_to_expiration', 'gamma_exposure', 'gamma_impact_score']].to_string())
        
        print("\n6. 📊 Creating Interactive Chart...")
        try:
            advanced.create_interactive_gamma_chart()
            print("✅ Interactive chart created (should open in browser)")
        except Exception as e:
            print(f"⚠️ Interactive chart failed (plotly might not be installed): {e}")
        
        return advanced
        
    except Exception as e:
        print(f"❌ Advanced features demo failed: {e}")
        return None

def quick_market_scan():
    """
    Quick scan of major market instruments
    """
    print("Quick Market Gamma Scan")
    print("=" * 60)
    
    # Major ETFs and popular stocks
    instruments = {
        'ETFs': ['SPY', 'QQQ', 'IWM', 'DIA'],
        'Mega Caps': ['AAPL', 'MSFT', 'GOOGL', 'AMZN'],
        'High Beta': ['TSLA', 'NVDA', 'AMD', 'NFLX']
    }
    
    all_results = {}
    
    for category, symbols in instruments.items():
        print(f"\n🔍 Scanning {category}...")
        results = create_gamma_scanner(symbols)
        if results:
            all_results[category] = results
    
    # Summary
    print(f"\n📋 Market Scan Summary")
    print("=" * 60)
    
    for category, results in all_results.items():
        print(f"\n{category}:")
        for symbol, data in results.items():
            regime_emoji = "🟡" if "Positive" in data['regime'] else "🟣" if "Negative" in data['regime'] else "⚪"
            print(f"  {regime_emoji} {symbol}: ${data['current_price']:.2f} | {data['regime'].split('-')[0].strip()}")
    
    return all_results

def educational_example():
    """
    Educational example showing step-by-step analysis
    """
    print("Educational Example: Understanding Gamma Exposure")
    print("=" * 60)
    
    symbol = "SPY"  # Use SPY as it has the most liquid options
    
    print(f"Let's analyze {symbol} step by step...")
    
    # Step 1: Create analyzer
    print("\n1️⃣ Creating Gamma Exposure Analyzer")
    analyzer = GammaExposureAnalyzer(symbol)
    
    # Step 2: Get current price
    print(f"2️⃣ Getting current {symbol} price")
    current_price = analyzer.get_current_price()
    print(f"   Current Price: ${current_price:.2f}")
    
    # Step 3: Fetch options data
    print(f"3️⃣ Fetching options data for {symbol}")
    options_data = analyzer.get_options_data()
    if options_data:
        total_options = sum(len(df) for df in options_data.values())
        print(f"   Total options contracts: {total_options}")
        print(f"   Expiration dates: {list(options_data.keys())}")
    
    # Step 4: Calculate gamma exposure
    print("4️⃣ Calculating gamma exposure")
    gamma_data = analyzer.calculate_gamma_exposure()
    if gamma_data is not None:
        print(f"   Processed {len(gamma_data)} options for gamma calculation")
    
    # Step 5: Analyze market sentiment
    print("5️⃣ Analyzing market sentiment")
    sentiment = analyzer.analyze_market_sentiment()
    if sentiment:
        print(f"   Market Regime: {sentiment['regime']}")
        print(f"   Net Gamma Exposure: ${sentiment['net_gamma']:,.0f}")
        
        if sentiment['net_gamma'] > 0:
            print("   💡 Interpretation: Dealers are net long gamma")
            print("      → Expect lower volatility and mean-reverting price action")
            print("      → Price moves will be dampened")
        else:
            print("   💡 Interpretation: Dealers are net short gamma")
            print("      → Expect higher volatility and trending price action")
            print("      → Price moves may be amplified")
    
    # Step 6: Identify key levels
    print("6️⃣ Identifying key gamma levels")
    levels = analyzer.identify_gamma_levels()
    if levels:
        if levels['king_node'] is not None:
            king_strike = levels['king_node']['strike']
            king_gamma = levels['king_node']['gamma_exposure']
            print(f"   👑 King Node: ${king_strike:.0f} (${king_gamma:,.0f} exposure)")
            
            if king_gamma > 0:
                print("      → This is a strong support/resistance level")
                print("      → Price may consolidate around this level")
            else:
                print("      → This could be a volatility catalyst")
                print("      → Price may react strongly when approaching this level")
        
        if levels['resistance_levels']:
            print(f"   📈 Key Resistance: {[f'${x:.0f}' for x in levels['resistance_levels'][:3]]}")
        
        if levels['support_levels']:
            print(f"   📉 Key Support: {[f'${x:.0f}' for x in levels['support_levels'][:3]]}")
    
    # Step 7: Generate trading signals
    print("7️⃣ Generating trading signals")
    signals = analyzer.generate_trading_signals()
    if signals:
        print("   🎯 Trading Signals:")
        for signal in signals:
            print(f"      {signal}")
    
    # Step 8: Create visualizations
    print("8️⃣ Creating visualizations")
    print("   📊 Gamma Profile Chart")
    analyzer.plot_gamma_profile()
    
    print("   🔥 Gamma Heatmap")
    analyzer.plot_gamma_exposure_heatmap()
    
    print(f"\n✅ Educational example completed!")
    print(f"💡 Key Takeaway: Gamma exposure helps predict how dealers will hedge,")
    print(f"   which influences price volatility and directional movement.")
    
    return analyzer

def main():
    """
    Main function with menu system
    """
    print("🔥 Gamma Exposure Analysis Tool 🔥")
    print("Based on HeatSeeker Methodology")
    print("=" * 60)
    
    while True:
        print("\nSelect an option:")
        print("1. 📊 Analyze Single Symbol")
        print("2. 🔍 Quick Market Scan")
        print("3. 📚 Educational Example (SPY)")
        print("4. 🚀 Advanced Features Demo")
        print("5. 📈 Test Multiple Symbols")
        print("6. ❌ Exit")
        
        try:
            choice = input("\nEnter your choice (1-6): ").strip()
            
            if choice == "1":
                symbol = input("Enter symbol (e.g., SPY, AAPL): ").strip().upper()
                if symbol:
                    test_single_symbol(symbol)
                else:
                    print("❌ Invalid symbol")
            
            elif choice == "2":
                quick_market_scan()
            
            elif choice == "3":
                educational_example()
            
            elif choice == "4":
                symbol = input("Enter symbol for advanced demo (default SPY): ").strip().upper()
                if not symbol:
                    symbol = "SPY"
                demo_advanced_features(symbol)
            
            elif choice == "5":
                test_multiple_symbols()
            
            elif choice == "6":
                print("👋 Thanks for using Gamma Exposure Analysis Tool!")
                break
            
            else:
                print("❌ Invalid choice. Please enter 1-6.")
                
        except KeyboardInterrupt:
            print("\n👋 Thanks for using Gamma Exposure Analysis Tool!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()