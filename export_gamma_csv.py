#!/usr/bin/env python3
"""
Standalone CSV Export Script for Gamma Exposure Analysis

Usage:
    python export_gamma_csv.py SPY                    # Export all SPY data
    python export_gamma_csv.py AAPL matrix           # Export only matrix for AAPL
    python export_gamma_csv.py QQQ strike            # Export only strike data for QQQ
    python export_gamma_csv.py TSLA expiration       # Export only expiration data for TSLA
"""

import sys
import os
from gamma_exposure_analyzer import GammaExposureAnalyzer
from csv_exporter import GammaExposureCSVExporter, create_gamma_exports

def main():
    """Main export function"""
    print("📊 Gamma Exposure CSV Export Utility")
    print("=" * 50)
    
    # Parse command line arguments
    if len(sys.argv) < 2:
        print("Usage: python export_gamma_csv.py <SYMBOL> [format]")
        print("\nFormats:")
        print("  all        - Export all formats (default)")
        print("  matrix     - Gamma matrix (strikes vs expirations)")
        print("  strike     - Aggregated by strike price")
        print("  expiration - Aggregated by expiration date")
        print("  raw        - Raw options data with gamma")
        print("  levels     - Key support/resistance levels")
        print("  summary    - Market summary")
        print("\nExamples:")
        print("  python export_gamma_csv.py SPY")
        print("  python export_gamma_csv.py AAPL matrix")
        print("  python export_gamma_csv.py QQQ strike")
        
        # Interactive mode
        symbol = input("\nEnter symbol: ").strip().upper()
        if not symbol:
            print("❌ No symbol provided")
            return
        export_format = "all"
    else:
        symbol = sys.argv[1].upper()
        export_format = sys.argv[2].lower() if len(sys.argv) > 2 else "all"
    
    # Validate format
    valid_formats = ["all", "matrix", "strike", "expiration", "raw", "levels", "summary"]
    if export_format not in valid_formats:
        print(f"❌ Invalid format: {export_format}")
        print(f"Valid formats: {', '.join(valid_formats)}")
        return
    
    print(f"🎯 Target: {symbol}")
    print(f"📁 Format: {export_format}")
    print()
    
    # Run export
    exported_files = create_gamma_exports(symbol, export_format)
    
    if exported_files:
        print(f"\n🎉 Export successful!")
        print(f"📂 Files created:")
        
        for filepath in exported_files:
            if filepath and os.path.exists(filepath):
                filename = os.path.basename(filepath)
                file_size = os.path.getsize(filepath) / 1024  # KB
                print(f"   📋 {filename} ({file_size:.1f} KB)")
                
        # Show directory location
        export_dir = os.path.dirname(exported_files[0]) if exported_files else None
        if export_dir:
            print(f"\n📁 Export directory: {export_dir}")
            print(f"💡 Open with: open {export_dir}")
    else:
        print(f"\n❌ Export failed")

def quick_export(symbol, format_type="all"):
    """
    Quick export function for programmatic use
    
    Args:
        symbol (str): Stock symbol
        format_type (str): Export format
    
    Returns:
        list: List of exported file paths
    """
    return create_gamma_exports(symbol, format_type)

if __name__ == "__main__":
    main()