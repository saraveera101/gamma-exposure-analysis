"""
Debug script to check key_levels structure
"""

from gamma_exposure_analyzer import GammaExposureAnalyzer
from advanced_analysis import AdvancedGammaAnalysis

def debug_key_levels():
    """Check what columns are in key_levels"""
    
    print("Testing key_levels structure...")
    
    # Test with SPY
    try:
        analyzer = GammaExposureAnalyzer("SPY")
        current_price = analyzer.get_current_price()
        print(f"Current SPY price: ${current_price:.2f}")
        
        # Get options data (minimal)
        options_data = analyzer.get_options_data()
        print(f"Found {len(options_data)} expiration dates")
        
        # Calculate minimal gamma
        gamma_data = analyzer.calculate_gamma_exposure()
        if gamma_data is not None:
            print(f"Calculated gamma for {len(gamma_data)} options")
            
            # Test advanced analysis
            advanced = AdvancedGammaAnalysis(analyzer)
            key_levels = advanced.calculate_gex_profile_levels(5)
            
            if key_levels is not None:
                print(f"\nKey levels shape: {key_levels.shape}")
                print("Available columns:")
                for col in key_levels.columns:
                    print(f"  - {col}")
                
                print("\nFirst few rows:")
                print(key_levels.head())
            else:
                print("No key levels returned")
        else:
            print("No gamma data returned")
            
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    debug_key_levels()