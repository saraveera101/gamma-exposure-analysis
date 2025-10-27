#!/usr/bin/env python3

"""
Quick test script to verify Vanna and Charm matrix creation
"""

from gamma_exposure_analyzer import GammaExposureAnalyzer

def test_matrices():
    print("Testing Vanna and Charm matrix creation...")
    
    # Create analyzer
    analyzer = GammaExposureAnalyzer("SPY")
    
    # Get current price
    current_price = analyzer.get_current_price()
    print(f"Current price: {current_price}")
    
    # Get options data
    options_data = analyzer.get_options_data()
    print(f"Options data loaded: {len(options_data)} expirations")
    
    # Calculate gamma exposure
    gamma_data = analyzer.calculate_gamma_exposure()
    print(f"Gamma data: {len(gamma_data) if gamma_data is not None else 'None'}")
    
    if gamma_data is not None and len(gamma_data) > 0:
        print(f"Columns in gamma_data: {gamma_data.columns.tolist()}")
        
        # Check if vanna_exposure and charm_exposure exist
        if 'vanna_exposure' in gamma_data.columns:
            print(f"Vanna exposure column exists with {(gamma_data['vanna_exposure'] != 0).sum()} non-zero values")
            print(f"Vanna exposure range: {gamma_data['vanna_exposure'].min()} to {gamma_data['vanna_exposure'].max()}")
        else:
            print("❌ Vanna exposure column missing!")
            
        if 'charm_exposure' in gamma_data.columns:
            print(f"Charm exposure column exists with {(gamma_data['charm_exposure'] != 0).sum()} non-zero values")
            print(f"Charm exposure range: {gamma_data['charm_exposure'].min()} to {gamma_data['charm_exposure'].max()}")
        else:
            print("❌ Charm exposure column missing!")
        
        # Test matrix aggregation methods
        print("\nTesting matrix aggregation...")
        
        vanna_matrix = analyzer.aggregate_vanna_by_expiration()
        print(f"Vanna matrix: {type(vanna_matrix)}, shape: {vanna_matrix.shape if vanna_matrix is not None else 'None'}")
        
        charm_matrix = analyzer.aggregate_charm_by_expiration()
        print(f"Charm matrix: {type(charm_matrix)}, shape: {charm_matrix.shape if charm_matrix is not None else 'None'}")
        
        if vanna_matrix is not None:
            print(f"Vanna matrix columns: {vanna_matrix.columns.tolist()[:5]}...")  # First 5 columns
            print(f"Vanna matrix index range: {vanna_matrix.index.min()} to {vanna_matrix.index.max()}")
            print(f"Vanna matrix non-zero values: {(vanna_matrix != 0).sum().sum()}")
        
        if charm_matrix is not None:
            print(f"Charm matrix columns: {charm_matrix.columns.tolist()[:5]}...")  # First 5 columns
            print(f"Charm matrix index range: {charm_matrix.index.min()} to {charm_matrix.index.max()}")
            print(f"Charm matrix non-zero values: {(charm_matrix != 0).sum().sum()}")
    
    else:
        print("❌ No gamma data calculated!")

if __name__ == "__main__":
    test_matrices()