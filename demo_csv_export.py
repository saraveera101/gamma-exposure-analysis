#!/usr/bin/env python3
"""
Quick demo of CSV export functionality
"""

from csv_exporter import create_gamma_exports
import os

def demo_csv_export():
    """Demonstrate CSV export with SPY"""
    print("🔥 CSV Export Demo")
    print("=" * 40)
    
    symbol = "SPY"
    print(f"📊 Exporting gamma data for {symbol}...")
    
    # Export all formats
    exported_files = create_gamma_exports(symbol, "all")
    
    if exported_files:
        print(f"\n✅ Demo completed successfully!")
        print(f"📁 Files created:")
        
        for filepath in exported_files:
            if filepath and os.path.exists(filepath):
                filename = os.path.basename(filepath)
                file_size = os.path.getsize(filepath) / 1024  # KB
                print(f"   📋 {filename} ({file_size:.1f} KB)")
        
        # Show sample of matrix file
        print(f"\n📊 Sample of gamma matrix data:")
        matrix_file = next((f for f in exported_files if "matrix" in f), None)
        if matrix_file and os.path.exists(matrix_file):
            with open(matrix_file, 'r') as f:
                lines = f.readlines()
                for i, line in enumerate(lines[:15]):  # Show first 15 lines
                    print(f"   {line.strip()}")
                if len(lines) > 15:
                    print(f"   ... ({len(lines)-15} more lines)")
    else:
        print("❌ Demo failed")

if __name__ == "__main__":
    demo_csv_export()