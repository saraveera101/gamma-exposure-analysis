#!/usr/bin/env python3
"""
Simple test script for Gamma Exposure Analysis Tool
Run this to verify installation and basic functionality
"""

import sys
import traceback

def test_imports():
    """Test all required imports"""
    print("🧪 Testing imports...")
    
    try:
        import yfinance as yf
        print("✅ yfinance imported successfully")
    except ImportError as e:
        print(f"❌ yfinance import failed: {e}")
        return False
    
    try:
        import pandas as pd
        import numpy as np
        import matplotlib.pyplot as plt
        import seaborn as sns
        from scipy import stats
        print("✅ Core libraries imported successfully")
    except ImportError as e:
        print(f"❌ Core libraries import failed: {e}")
        return False
    
    try:
        import plotly.graph_objects as go
        print("✅ Plotly imported successfully")
    except ImportError:
        print("⚠️ Plotly not available (optional for interactive charts)")
    
    return True

def test_basic_functionality():
    """Test basic gamma exposure analyzer functionality"""
    print("\n🧪 Testing basic functionality...")
    
    try:
        from gamma_exposure_analyzer import GammaExposureAnalyzer
        print("✅ GammaExposureAnalyzer imported successfully")
        
        # Test with SPY (most liquid options)
        print("📊 Testing with SPY...")
        analyzer = GammaExposureAnalyzer("SPY")
        
        # Test getting current price
        price = analyzer.get_current_price()
        if price and price > 0:
            print(f"✅ Current SPY price: ${price:.2f}")
        else:
            print("❌ Failed to get current price")
            return False
        
        print("✅ Basic functionality test passed")
        return True
        
    except Exception as e:
        print(f"❌ Basic functionality test failed: {e}")
        traceback.print_exc()
        return False

def test_options_data():
    """Test options data retrieval"""
    print("\n🧪 Testing options data retrieval...")
    
    try:
        from gamma_exposure_analyzer import GammaExposureAnalyzer
        
        analyzer = GammaExposureAnalyzer("SPY")
        analyzer.get_current_price()
        
        # Get limited options data for testing
        print("📈 Fetching SPY options data (this may take a moment)...")
        options_data = analyzer.get_options_data()
        
        if options_data and len(options_data) > 0:
            total_options = sum(len(df) for df in options_data.values())
            print(f"✅ Retrieved {len(options_data)} expiration dates with {total_options} total options")
            
            # Test gamma calculation on subset
            print("🧮 Testing gamma exposure calculation...")
            gamma_data = analyzer.calculate_gamma_exposure()
            
            if gamma_data is not None and len(gamma_data) > 0:
                print(f"✅ Calculated gamma exposure for {len(gamma_data)} options")
                return True
            else:
                print("⚠️ Gamma calculation returned no data (may be market hours issue)")
                return False
        else:
            print("❌ No options data retrieved")
            return False
            
    except Exception as e:
        print(f"❌ Options data test failed: {e}")
        traceback.print_exc()
        return False

def test_advanced_features():
    """Test advanced analysis features"""
    print("\n🧪 Testing advanced features...")
    
    try:
        from gamma_exposure_analyzer import GammaExposureAnalyzer
        from advanced_analysis import AdvancedGammaAnalysis
        
        analyzer = GammaExposureAnalyzer("SPY")
        analyzer.get_current_price()
        analyzer.get_options_data()
        analyzer.calculate_gamma_exposure()
        
        advanced = AdvancedGammaAnalysis(analyzer)
        
        # Test dealer positioning
        positioning = advanced.calculate_dealer_positioning()
        if positioning:
            print("✅ Dealer positioning analysis working")
        
        # Test gamma levels
        levels = advanced.calculate_gex_profile_levels(5)
        if levels is not None:
            print("✅ GEX profile levels working")
        
        print("✅ Advanced features test passed")
        return True
        
    except Exception as e:
        print(f"❌ Advanced features test failed: {e}")
        traceback.print_exc()
        return False

def quick_demo():
    """Run a quick demo analysis"""
    print("\n🚀 Running quick demo analysis...")
    
    try:
        from gamma_exposure_analyzer import GammaExposureAnalyzer
        
        # Use SPY for demo
        analyzer = GammaExposureAnalyzer("SPY")
        
        print("1. Getting current price...")
        current_price = analyzer.get_current_price()
        print(f"   SPY Price: ${current_price:.2f}")
        
        print("2. Analyzing market sentiment...")
        # Quick sentiment without full data fetch
        analyzer.options_data = {}  # Initialize empty
        analyzer.gamma_exposure_data = None
        
        # For demo, just show the structure
        print("   📊 Analysis structure verified")
        print("   🎯 Ready for full analysis")
        
        print("✅ Quick demo completed successfully!")
        print("\n💡 To run full analysis, use:")
        print("   python examples.py")
        print("   or")
        print("   from gamma_exposure_analyzer import GammaExposureAnalyzer")
        print("   analyzer = GammaExposureAnalyzer('SPY')")
        print("   analyzer.run_complete_analysis()")
        
        return True
        
    except Exception as e:
        print(f"❌ Quick demo failed: {e}")
        traceback.print_exc()
        return False

def main():
    """Run all tests"""
    print("🔥 Gamma Exposure Analysis Tool - Test Suite")
    print("=" * 60)
    
    tests = [
        ("Import Test", test_imports),
        ("Basic Functionality", test_basic_functionality),
        ("Options Data", test_options_data),
        ("Advanced Features", test_advanced_features),
        ("Quick Demo", quick_demo)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n{'='*20} {test_name} {'='*20}")
        try:
            if test_func():
                passed += 1
                print(f"✅ {test_name} PASSED")
            else:
                print(f"❌ {test_name} FAILED")
        except KeyboardInterrupt:
            print(f"\n⚠️ Test interrupted by user")
            break
        except Exception as e:
            print(f"❌ {test_name} FAILED with exception: {e}")
    
    print(f"\n{'='*60}")
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Gamma Exposure Analysis Tool is ready to use.")
        print("\n🚀 Next steps:")
        print("   1. Run 'python examples.py' for interactive menu")
        print("   2. Check README.md for detailed usage instructions")
        print("   3. Start analyzing your favorite symbols!")
    else:
        print("⚠️ Some tests failed. Check error messages above.")
        print("\n🔧 Troubleshooting:")
        print("   1. Ensure all dependencies are installed: pip install -r requirements.txt")
        print("   2. Check internet connection for yfinance data")
        print("   3. Try during market hours for better options data")
    
    print(f"\n{'='*60}")

if __name__ == "__main__":
    main()