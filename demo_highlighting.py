"""
Test script to demonstrate the enhanced Streamlit gamma matrix highlighting
"""

import pandas as pd
import numpy as np

def demo_highlighting():
    """Create a sample gamma matrix to show highlighting functionality"""
    
    # Create sample data similar to what the app would generate
    strikes = [300, 310, 320, 330, 340, 350, 360, 370, 380]
    expirations = ['2025-11-01', '2025-11-15', '2025-12-01']
    
    # Sample gamma exposure data
    data = {
        '2025-11-01': [5000, -12000, 8000, -3000, 15000, -8000, 2000, -1000, 500],
        '2025-11-15': [3000, -8000, 12000, -15000, 6000, -4000, 1000, -500, 200],
        '2025-12-01': [2000, -5000, 6000, -8000, 18000, -12000, 3000, -2000, 800]
    }
    
    df = pd.DataFrame(data, index=strikes)
    
    print("Sample Gamma Matrix (USD):")
    print("=" * 60)
    print(df)
    
    print("\nHighlighting Analysis:")
    print("=" * 60)
    
    for col in df.columns:
        col_data = df[col]
        non_zero_data = col_data[col_data != 0]
        
        if len(non_zero_data) > 0:
            max_val = non_zero_data.max()
            min_val = non_zero_data.min()
            max_strike = col_data.idxmax()
            min_strike = col_data.idxmin()
            
            print(f"\n{col}:")
            print(f"  🟢 Highest Positive: ${max_val:,} at strike ${max_strike}")
            print(f"  🔴 Highest Negative: ${min_val:,} at strike ${min_strike}")

if __name__ == "__main__":
    demo_highlighting()