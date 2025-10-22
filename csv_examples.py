"""
Example CSV Output Formats for Gamma Exposure Analysis

This file shows examples of what each CSV export format contains.
"""

# Example 1: Raw Gamma Data CSV
RAW_GAMMA_DATA_EXAMPLE = """
symbol,analysis_timestamp,current_price,expiration,days_to_expiration,strike,type,gamma_exposure,vanna_exposure,open_interest,implied_volatility,delta,gamma,vanna,last_price,volume
SPY,2025-10-21 12:00:00,428.50,2025-10-25,4,425.0,call,-125000.5,45000.2,1250,0.185,0.52,0.0123,-0.025,2.85,342
SPY,2025-10-21 12:00:00,428.50,2025-10-25,4,430.0,call,-87500.3,32000.1,875,0.178,0.38,0.0089,-0.019,1.92,156
SPY,2025-10-21 12:00:00,428.50,2025-10-25,4,425.0,put,95000.8,-38000.5,950,0.192,0.48,0.0115,0.022,2.15,298
"""

# Example 2: Gamma Matrix CSV (Strikes vs Expirations)
GAMMA_MATRIX_EXAMPLE = """
# Gamma Exposure Matrix for SPY
# Analysis Date: 2025-10-21 12:00:00
# Current Price: $428.50
# Values in USD (Gamma Exposure)
# Rows: Strike Prices
# Columns: Expiration Dates
#
strike,2025-10-25,2025-11-01,2025-11-15,2025-12-20
420.0,45000.2,12000.5,-8500.3,25000.8
425.0,125000.8,35000.2,15000.6,45000.3
430.0,-87500.3,-25000.1,-12000.8,-35000.2
435.0,-145000.5,-45000.3,-22000.1,-55000.6
"""

# Example 3: Gamma by Strike CSV
GAMMA_BY_STRIKE_EXAMPLE = """
symbol,analysis_timestamp,current_price,strike,gamma_exposure,vanna_exposure,open_interest,abs_gamma_exposure,is_king_node,distance_from_current,distance_pct,above_below_current
SPY,2025-10-21 12:00:00,428.50,420.0,125000.8,45000.3,2850,125000.8,False,8.5,1.98,Below
SPY,2025-10-21 12:00:00,428.50,425.0,87500.5,32000.1,1950,87500.5,False,3.5,0.82,Below
SPY,2025-10-21 12:00:00,428.50,430.0,-145000.2,-55000.8,3250,145000.2,True,1.5,0.35,Above
SPY,2025-10-21 12:00:00,428.50,435.0,-98500.3,-42000.5,1850,98500.3,False,6.5,1.52,Above
"""

# Example 4: Gamma by Expiration CSV
GAMMA_BY_EXPIRATION_EXAMPLE = """
symbol,analysis_timestamp,current_price,expiration,days_to_expiration,options_count,total_gamma_exposure,avg_gamma_exposure,std_gamma_exposure,total_vanna_exposure,avg_vanna_exposure,total_open_interest,gamma_impact_score
SPY,2025-10-21 12:00:00,428.50,2025-10-25,4,245,-125000.8,-510.2,45000.3,85000.5,346.9,125850,31250.2
SPY,2025-10-21 12:00:00,428.50,2025-11-01,11,389,45000.3,115.7,32000.1,-25000.8,-64.3,89650,4090.9
SPY,2025-10-21 12:00:00,428.50,2025-11-15,25,456,85500.2,187.5,28000.5,65000.3,142.5,156850,3420.0
SPY,2025-10-21 12:00:00,428.50,2025-12-20,60,678,-65000.1,-95.9,22000.8,-45000.2,-66.4,245850,1083.3
"""

# Example 5: Key Levels CSV
KEY_LEVELS_EXAMPLE = """
symbol,analysis_timestamp,current_price,level_type,strike,gamma_exposure,vanna_exposure,open_interest,distance_from_current,distance_pct,above_below
SPY,2025-10-21 12:00:00,428.50,King Node,430.0,-145000.2,-55000.8,3250,1.5,0.35,Above
SPY,2025-10-21 12:00:00,428.50,Resistance_1,435.0,-98500.3,-42000.5,1850,6.5,1.52,Above
SPY,2025-10-21 12:00:00,428.50,Resistance_2,440.0,-75000.8,-35000.2,1250,11.5,2.68,Above
SPY,2025-10-21 12:00:00,428.50,Support_1,425.0,87500.5,32000.1,1950,3.5,0.82,Below
SPY,2025-10-21 12:00:00,428.50,Support_2,420.0,125000.8,45000.3,2850,8.5,1.98,Below
"""

# Example 6: Market Summary CSV
MARKET_SUMMARY_EXAMPLE = """
symbol,analysis_timestamp,current_price,market_regime,regime_color,net_gamma_exposure,total_positive_gamma,total_negative_gamma,near_money_gamma,gamma_flip_points_count,gamma_flip_points
SPY,2025-10-21 12:00:00,428.50,Positive Gamma Environment - Expect Lower Volatility,🟡,125000.5,485000.8,-360000.3,87500.2,2,$425; $435
"""

def show_csv_examples():
    """Display examples of each CSV format"""
    print("📊 CSV Export Format Examples")
    print("=" * 60)
    
    examples = [
        ("1. Raw Gamma Data", RAW_GAMMA_DATA_EXAMPLE),
        ("2. Gamma Matrix", GAMMA_MATRIX_EXAMPLE),
        ("3. Gamma by Strike", GAMMA_BY_STRIKE_EXAMPLE),
        ("4. Gamma by Expiration", GAMMA_BY_EXPIRATION_EXAMPLE),
        ("5. Key Levels", KEY_LEVELS_EXAMPLE),
        ("6. Market Summary", MARKET_SUMMARY_EXAMPLE)
    ]
    
    for title, example in examples:
        print(f"\n{title}:")
        print("-" * 40)
        print(example.strip())
        print()

def describe_csv_formats():
    """Describe what each CSV format contains"""
    print("📋 CSV Format Descriptions")
    print("=" * 50)
    
    descriptions = {
        "Raw Gamma Data": {
            "purpose": "Complete dataset with all options and calculated Greeks",
            "use_case": "Detailed analysis, custom calculations, backtesting",
            "columns": "Symbol, timestamp, expiration, strike, type, gamma exposure, Greeks, open interest",
            "size": "Large (thousands of rows for liquid symbols)"
        },
        
        "Gamma Matrix": {
            "purpose": "Heatmap-style data showing gamma exposure by strike and expiration",
            "use_case": "Visual analysis, identifying concentration areas",
            "columns": "Strike prices as rows, expiration dates as columns, gamma exposure as values",
            "size": "Medium (strikes × expirations matrix)"
        },
        
        "Gamma by Strike": {
            "purpose": "Aggregated gamma exposure for each strike price across all expirations",
            "use_case": "Identifying key support/resistance levels",
            "columns": "Strike, total gamma exposure, distance from current price, king node flag",
            "size": "Small (one row per strike price)"
        },
        
        "Gamma by Expiration": {
            "purpose": "Aggregated gamma exposure for each expiration date",
            "use_case": "Understanding time decay effects, expiration impact",
            "columns": "Expiration date, days to expiry, total gamma, impact score",
            "size": "Small (one row per expiration)"
        },
        
        "Key Levels": {
            "purpose": "Summary of most important gamma levels (king nodes, support, resistance)",
            "use_case": "Quick reference for trading decisions",
            "columns": "Level type, strike, gamma exposure, distance from current price",
            "size": "Very small (5-10 key levels)"
        },
        
        "Market Summary": {
            "purpose": "Overall market analysis and regime identification",
            "use_case": "High-level market assessment, regime detection",
            "columns": "Symbol, regime, net gamma, gamma flip points",
            "size": "Single row summary"
        }
    }
    
    for format_name, info in descriptions.items():
        print(f"\n📊 {format_name}")
        print(f"   Purpose: {info['purpose']}")
        print(f"   Use Case: {info['use_case']}")
        print(f"   Columns: {info['columns']}")
        print(f"   Size: {info['size']}")

if __name__ == "__main__":
    show_csv_examples()
    print("\n" + "=" * 60)
    describe_csv_formats()