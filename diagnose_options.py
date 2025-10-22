#!/usr/bin/env python3
"""
Diagnostic script to check options data quality and gamma calculation issues
"""

import yfinance as yf
import pandas as pd
import numpy as np
from gamma_exposure_analyzer import GammaExposureAnalyzer

def diagnose_symbol(symbol):
    """
    Diagnose options data issues for a given symbol
    """
    print(f"🔍 Diagnosing {symbol} Options Data")
    print("=" * 50)
    
    try:
        # Create analyzer
        analyzer = GammaExposureAnalyzer(symbol)
        
        # Step 1: Get current price
        print("1️⃣ Getting current price...")
        current_price = analyzer.get_current_price()
        print(f"   Current Price: ${current_price:.2f}")
        
        # Step 2: Fetch raw options data
        print("\n2️⃣ Fetching options data...")
        ticker = yf.Ticker(symbol)
        expirations = ticker.options
        print(f"   Available expirations: {len(expirations)}")
        
        if not expirations:
            print("❌ No options expirations found!")
            return
        
        # Check first few expirations
        for i, exp_date in enumerate(expirations[:3]):
            print(f"\n   📅 Checking {exp_date}...")
            try:
                option_chain = ticker.option_chain(exp_date)
                calls = option_chain.calls
                puts = option_chain.puts
                
                print(f"      Calls: {len(calls)} contracts")
                print(f"      Puts: {len(puts)} contracts")
                
                # Check calls data quality
                calls_with_oi = calls[calls['openInterest'] > 0]
                calls_with_iv = calls[calls['impliedVolatility'] > 0]
                print(f"      Calls with OI > 0: {len(calls_with_oi)}")
                print(f"      Calls with IV > 0: {len(calls_with_iv)}")
                
                # Check puts data quality
                puts_with_oi = puts[puts['openInterest'] > 0]
                puts_with_iv = puts[puts['impliedVolatility'] > 0]
                print(f"      Puts with OI > 0: {len(puts_with_oi)}")
                print(f"      Puts with IV > 0: {len(puts_with_iv)}")
                
                # Show sample data
                if len(calls_with_oi) > 0:
                    sample_call = calls_with_oi.iloc[0]
                    print(f"      Sample call: ${sample_call['strike']:.0f}, OI={sample_call['openInterest']}, IV={sample_call['impliedVolatility']:.3f}")
                
                if len(puts_with_oi) > 0:
                    sample_put = puts_with_oi.iloc[0]
                    print(f"      Sample put: ${sample_put['strike']:.0f}, OI={sample_put['openInterest']}, IV={sample_put['impliedVolatility']:.3f}")
                
            except Exception as e:
                print(f"      ❌ Error fetching {exp_date}: {e}")
        
        # Step 3: Run full analysis
        print(f"\n3️⃣ Running full analysis...")
        analyzer.get_options_data()
        gamma_data = analyzer.calculate_gamma_exposure()
        
        if gamma_data is not None and len(gamma_data) > 0:
            print(f"✅ Gamma calculation successful!")
            print(f"   Total records: {len(gamma_data)}")
            print(f"   Unique strikes: {gamma_data['strike'].nunique()}")
            print(f"   Unique expirations: {gamma_data['expiration'].nunique()}")
            
            # Check gamma exposure values
            non_zero_gamma = gamma_data[gamma_data['gamma_exposure'] != 0]
            print(f"   Non-zero gamma exposures: {len(non_zero_gamma)}")
            
            if len(non_zero_gamma) > 0:
                print(f"   Gamma range: ${non_zero_gamma['gamma_exposure'].min():,.0f} to ${non_zero_gamma['gamma_exposure'].max():,.0f}")
                print(f"   Total net gamma: ${gamma_data['gamma_exposure'].sum():,.0f}")
                
                # Test matrix creation
                print(f"\n4️⃣ Testing matrix creation...")
                gamma_matrix = analyzer.aggregate_gamma_by_expiration()
                if gamma_matrix is not None:
                    print(f"   Matrix shape: {gamma_matrix.shape}")
                    print(f"   Non-zero values in matrix: {(gamma_matrix != 0).sum().sum()}")
                    if (gamma_matrix != 0).sum().sum() > 0:
                        print(f"   ✅ Matrix has data!")
                    else:
                        print(f"   ❌ Matrix is empty (all zeros)")
                else:
                    print(f"   ❌ Matrix creation failed")
            else:
                print(f"   ❌ All gamma exposures are zero")
        else:
            print(f"❌ Gamma calculation failed!")
            
    except Exception as e:
        print(f"❌ Diagnosis failed: {e}")
        import traceback
        traceback.print_exc()

def compare_symbols():
    """Compare multiple symbols to see which ones work"""
    symbols = ["SPY", "AAPL", "TSLA", "NFLX", "QQQ"]
    
    print("🔍 Comparing Multiple Symbols")
    print("=" * 50)
    
    results = {}
    
    for symbol in symbols:
        print(f"\n📊 Testing {symbol}...")
        try:
            analyzer = GammaExposureAnalyzer(symbol)
            analyzer.get_current_price()
            analyzer.get_options_data()
            gamma_data = analyzer.calculate_gamma_exposure()
            
            if gamma_data is not None:
                non_zero = (gamma_data['gamma_exposure'] != 0).sum()
                results[symbol] = {
                    'status': '✅ Success',
                    'records': len(gamma_data),
                    'non_zero_gamma': non_zero,
                    'net_gamma': gamma_data['gamma_exposure'].sum()
                }
            else:
                results[symbol] = {
                    'status': '❌ Failed',
                    'records': 0,
                    'non_zero_gamma': 0,
                    'net_gamma': 0
                }
                
        except Exception as e:
            results[symbol] = {
                'status': f'❌ Error: {str(e)[:50]}',
                'records': 0,
                'non_zero_gamma': 0,
                'net_gamma': 0
            }
    
    print(f"\n📋 Summary Results:")
    print("-" * 60)
    for symbol, data in results.items():
        print(f"{symbol:6} | {data['status']:15} | Records: {data['records']:4} | Non-zero: {data['non_zero_gamma']:4} | Net: ${data['net_gamma']:>10,.0f}")

def main():
    """Main diagnostic function"""
    print("🔧 Gamma Exposure Diagnostic Tool")
    print("=" * 50)
    
    choice = input("Choose:\n1. Diagnose specific symbol\n2. Compare multiple symbols\nChoice (1/2): ").strip()
    
    if choice == "1":
        symbol = input("Enter symbol to diagnose: ").strip().upper()
        if symbol:
            diagnose_symbol(symbol)
        else:
            print("❌ No symbol provided")
    elif choice == "2":
        compare_symbols()
    else:
        print("❌ Invalid choice")

if __name__ == "__main__":
    main()