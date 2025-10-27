#!/usr/bin/env python3
"""Quick test to verify charm column exists"""

from gamma_exposure_analyzer import GammaExposureAnalyzer

# Create analyzer and calculate one test exposure
analyzer = GammaExposureAnalyzer("SPY")
current_price = analyzer.get_current_price()

# Test Black-Scholes Greeks method
greeks = analyzer.black_scholes_greeks(
    S=current_price, 
    K=current_price, 
    T=0.1, 
    r=0.05, 
    sigma=0.2, 
    option_type='call'
)

print("Greeks calculated:")
for key, value in greeks.items():
    print(f"  {key}: {value}")

print(f"\nAll expected Greeks present: {all(key in greeks for key in ['delta', 'gamma', 'vanna', 'charm'])}")