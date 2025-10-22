"""
CSV Export Module for Gamma Exposure Analysis
Exports gamma exposure data by expiration date and strike to CSV files
"""

import pandas as pd
import numpy as np
from datetime import datetime
import os
from gamma_exposure_analyzer import GammaExposureAnalyzer
from advanced_analysis import AdvancedGammaAnalysis

class GammaExposureCSVExporter:
    """
    Export gamma exposure data to CSV files in various formats
    """
    
    def __init__(self, analyzer):
        self.analyzer = analyzer
        self.symbol = analyzer.symbol
        self.export_dir = f"gamma_exports_{self.symbol}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
    def create_export_directory(self):
        """Create directory for exports"""
        if not os.path.exists(self.export_dir):
            os.makedirs(self.export_dir)
            print(f"📁 Created export directory: {self.export_dir}")
        return self.export_dir
    
    def export_raw_gamma_data(self, filename=None):
        """
        Export raw gamma exposure data with all details
        """
        if self.analyzer.gamma_exposure_data is None:
            print("❌ No gamma exposure data available. Run analysis first.")
            return None
        
        if filename is None:
            filename = f"{self.symbol}_raw_gamma_data.csv"
        
        filepath = os.path.join(self.export_dir, filename)
        
        # Prepare data for export
        export_data = self.analyzer.gamma_exposure_data.copy()
        
        # Add current price and timestamp
        export_data['current_price'] = self.analyzer.current_price
        export_data['analysis_timestamp'] = datetime.now()
        export_data['symbol'] = self.symbol
        
        # Reorder columns for better readability
        column_order = [
            'symbol', 'analysis_timestamp', 'current_price',
            'expiration', 'days_to_expiration', 'strike', 'type',
            'gamma_exposure', 'vanna_exposure', 'open_interest',
            'implied_volatility', 'delta', 'gamma', 'vanna',
            'last_price', 'volume'
        ]
        
        # Ensure all columns exist
        for col in column_order:
            if col not in export_data.columns:
                export_data[col] = None
        
        export_data = export_data[column_order]
        
        # Export to CSV
        export_data.to_csv(filepath, index=False)
        print(f"✅ Raw gamma data exported to: {filepath}")
        print(f"   Records: {len(export_data)}")
        
        return filepath
    
    def export_gamma_matrix(self, filename=None):
        """
        Export gamma exposure matrix (strikes vs expirations)
        """
        gamma_matrix = self.analyzer.aggregate_gamma_by_expiration()
        if gamma_matrix is None:
            print("❌ No gamma matrix data available.")
            return None
        
        # Check if matrix has any data
        if gamma_matrix.empty or gamma_matrix.isna().all().all():
            print("❌ Gamma matrix is empty - no valid gamma exposure data calculated.")
            print("💡 This could be due to:")
            print("   - No options data available")
            print("   - All options have zero open interest")
            print("   - Missing implied volatility data")
            print("   - Issues with options data quality")
            return None
        
        if filename is None:
            filename = f"{self.symbol}_gamma_matrix.csv"
        
        filepath = os.path.join(self.export_dir, filename)
        
        # Debug information
        print(f"📊 Matrix dimensions: {gamma_matrix.shape[0]} strikes × {gamma_matrix.shape[1]} expirations")
        print(f"📊 Non-zero values: {(gamma_matrix != 0).sum().sum()}")
        print(f"📊 Value range: ${gamma_matrix.min().min():,.0f} to ${gamma_matrix.max().max():,.0f}")
        
        # Add metadata as header comments
        with open(filepath, 'w') as f:
            f.write(f"# Gamma Exposure Matrix for {self.symbol}\n")
            f.write(f"# Analysis Date: {datetime.now()}\n")
            f.write(f"# Current Price: ${self.analyzer.current_price:.2f}\n")
            f.write(f"# Values in USD (Gamma Exposure)\n")
            f.write(f"# Rows: Strike Prices\n")
            f.write(f"# Columns: Expiration Dates\n")
            f.write(f"# Matrix Size: {gamma_matrix.shape[0]} strikes × {gamma_matrix.shape[1]} expirations\n")
            f.write(f"# Non-zero values: {(gamma_matrix != 0).sum().sum()}\n")
            f.write("#\n")
        
        # Export matrix with header
        gamma_matrix.to_csv(filepath, mode='a')
        print(f"✅ Gamma matrix exported to: {filepath}")
        print(f"   Dimensions: {gamma_matrix.shape[0]} strikes × {gamma_matrix.shape[1]} expirations")
        
        return filepath
    
    def export_gamma_by_strike(self, filename=None):
        """
        Export aggregated gamma exposure by strike price
        """
        gamma_by_strike = self.analyzer.aggregate_gamma_by_strike()
        if gamma_by_strike is None:
            print("❌ No gamma by strike data available.")
            return None
        
        if filename is None:
            filename = f"{self.symbol}_gamma_by_strike.csv"
        
        filepath = os.path.join(self.export_dir, filename)
        
        # Add metadata
        export_data = gamma_by_strike.copy()
        export_data['symbol'] = self.symbol
        export_data['current_price'] = self.analyzer.current_price
        export_data['analysis_timestamp'] = datetime.now()
        
        # Calculate additional metrics
        export_data['distance_from_current'] = abs(export_data['strike'] - self.analyzer.current_price)
        export_data['distance_pct'] = export_data['distance_from_current'] / self.analyzer.current_price * 100
        export_data['above_below_current'] = np.where(
            export_data['strike'] > self.analyzer.current_price, 'Above', 'Below'
        )
        
        # Reorder columns
        column_order = [
            'symbol', 'analysis_timestamp', 'current_price',
            'strike', 'gamma_exposure', 'vanna_exposure', 'open_interest',
            'abs_gamma_exposure', 'is_king_node',
            'distance_from_current', 'distance_pct', 'above_below_current'
        ]
        
        export_data = export_data[column_order]
        export_data = export_data.sort_values('strike')
        
        # Export to CSV
        export_data.to_csv(filepath, index=False)
        print(f"✅ Gamma by strike exported to: {filepath}")
        print(f"   Strikes: {len(export_data)}")
        
        return filepath
    
    def export_gamma_by_expiration(self, filename=None):
        """
        Export aggregated gamma exposure by expiration date
        """
        if self.analyzer.gamma_exposure_data is None:
            print("❌ No gamma exposure data available.")
            return None
        
        if filename is None:
            filename = f"{self.symbol}_gamma_by_expiration.csv"
        
        filepath = os.path.join(self.export_dir, filename)
        
        # Aggregate by expiration
        gamma_by_exp = self.analyzer.gamma_exposure_data.groupby('expiration').agg({
            'gamma_exposure': ['sum', 'count', 'mean', 'std'],
            'vanna_exposure': ['sum', 'mean'],
            'open_interest': 'sum',
            'days_to_expiration': 'first'
        }).reset_index()
        
        # Flatten column names
        gamma_by_exp.columns = ['expiration', 
                               'total_gamma_exposure', 'options_count', 'avg_gamma_exposure', 'std_gamma_exposure',
                               'total_vanna_exposure', 'avg_vanna_exposure',
                               'total_open_interest', 'days_to_expiration']
        
        # Add metadata
        gamma_by_exp['symbol'] = self.symbol
        gamma_by_exp['current_price'] = self.analyzer.current_price
        gamma_by_exp['analysis_timestamp'] = datetime.now()
        
        # Calculate gamma impact score (gamma exposure / days to expiry)
        gamma_by_exp['gamma_impact_score'] = abs(gamma_by_exp['total_gamma_exposure']) / gamma_by_exp['days_to_expiration'].replace(0, 1)
        
        # Sort by days to expiration
        gamma_by_exp = gamma_by_exp.sort_values('days_to_expiration')
        
        # Reorder columns
        column_order = [
            'symbol', 'analysis_timestamp', 'current_price',
            'expiration', 'days_to_expiration', 'options_count',
            'total_gamma_exposure', 'avg_gamma_exposure', 'std_gamma_exposure',
            'total_vanna_exposure', 'avg_vanna_exposure',
            'total_open_interest', 'gamma_impact_score'
        ]
        
        gamma_by_exp = gamma_by_exp[column_order]
        
        # Export to CSV
        gamma_by_exp.to_csv(filepath, index=False)
        print(f"✅ Gamma by expiration exported to: {filepath}")
        print(f"   Expirations: {len(gamma_by_exp)}")
        
        return filepath
    
    def export_key_levels(self, filename=None):
        """
        Export key gamma levels (king nodes, support, resistance)
        """
        levels = self.analyzer.identify_gamma_levels()
        if not levels:
            print("❌ No key levels data available.")
            return None
        
        if filename is None:
            filename = f"{self.symbol}_key_levels.csv"
        
        filepath = os.path.join(self.export_dir, filename)
        
        # Prepare key levels data
        key_levels_data = []
        
        # King node
        if levels['king_node'] is not None:
            king_data = levels['king_node'].copy()
            key_levels_data.append({
                'level_type': 'King Node',
                'strike': king_data['strike'],
                'gamma_exposure': king_data['gamma_exposure'],
                'vanna_exposure': king_data.get('vanna_exposure', 0),
                'open_interest': king_data.get('open_interest', 0),
                'distance_from_current': abs(king_data['strike'] - self.analyzer.current_price),
                'distance_pct': abs(king_data['strike'] - self.analyzer.current_price) / self.analyzer.current_price * 100,
                'above_below': 'Above' if king_data['strike'] > self.analyzer.current_price else 'Below'
            })
        
        # Resistance levels
        for i, strike in enumerate(levels['resistance_levels'][:5]):  # Top 5
            gamma_data = self.analyzer.aggregate_gamma_by_strike()
            if gamma_data is not None:
                strike_data = gamma_data[gamma_data['strike'] == strike]
                if len(strike_data) > 0:
                    row = strike_data.iloc[0]
                    key_levels_data.append({
                        'level_type': f'Resistance_{i+1}',
                        'strike': strike,
                        'gamma_exposure': row['gamma_exposure'],
                        'vanna_exposure': row.get('vanna_exposure', 0),
                        'open_interest': row.get('open_interest', 0),
                        'distance_from_current': abs(strike - self.analyzer.current_price),
                        'distance_pct': abs(strike - self.analyzer.current_price) / self.analyzer.current_price * 100,
                        'above_below': 'Above'
                    })
        
        # Support levels
        for i, strike in enumerate(levels['support_levels'][:5]):  # Top 5
            gamma_data = self.analyzer.aggregate_gamma_by_strike()
            if gamma_data is not None:
                strike_data = gamma_data[gamma_data['strike'] == strike]
                if len(strike_data) > 0:
                    row = strike_data.iloc[0]
                    key_levels_data.append({
                        'level_type': f'Support_{i+1}',
                        'strike': strike,
                        'gamma_exposure': row['gamma_exposure'],
                        'vanna_exposure': row.get('vanna_exposure', 0),
                        'open_interest': row.get('open_interest', 0),
                        'distance_from_current': abs(strike - self.analyzer.current_price),
                        'distance_pct': abs(strike - self.analyzer.current_price) / self.analyzer.current_price * 100,
                        'above_below': 'Below'
                    })
        
        if not key_levels_data:
            print("❌ No key levels found.")
            return None
        
        # Create DataFrame
        key_levels_df = pd.DataFrame(key_levels_data)
        
        # Add metadata
        key_levels_df['symbol'] = self.symbol
        key_levels_df['current_price'] = self.analyzer.current_price
        key_levels_df['analysis_timestamp'] = datetime.now()
        
        # Reorder columns
        column_order = [
            'symbol', 'analysis_timestamp', 'current_price',
            'level_type', 'strike', 'gamma_exposure', 'vanna_exposure', 'open_interest',
            'distance_from_current', 'distance_pct', 'above_below'
        ]
        
        key_levels_df = key_levels_df[column_order]
        key_levels_df = key_levels_df.sort_values('distance_from_current')
        
        # Export to CSV
        key_levels_df.to_csv(filepath, index=False)
        print(f"✅ Key levels exported to: {filepath}")
        print(f"   Levels: {len(key_levels_df)}")
        
        return filepath
    
    def export_market_summary(self, filename=None):
        """
        Export market summary and sentiment analysis
        """
        sentiment = self.analyzer.analyze_market_sentiment()
        if not sentiment:
            print("❌ No market sentiment data available.")
            return None
        
        if filename is None:
            filename = f"{self.symbol}_market_summary.csv"
        
        filepath = os.path.join(self.export_dir, filename)
        
        # Create summary data
        summary_data = [{
            'symbol': self.symbol,
            'analysis_timestamp': datetime.now(),
            'current_price': self.analyzer.current_price,
            'market_regime': sentiment['regime'],
            'regime_color': sentiment['color'],
            'net_gamma_exposure': sentiment['net_gamma'],
            'total_positive_gamma': sentiment['total_positive_gamma'],
            'total_negative_gamma': sentiment['total_negative_gamma'],
            'near_money_gamma': sentiment['near_money_gamma'],
            'gamma_flip_points_count': len(sentiment['gamma_flip_points']),
            'gamma_flip_points': '; '.join([f"${point['strike']:.0f}" for point in sentiment['gamma_flip_points']]) if sentiment['gamma_flip_points'] else 'None'
        }]
        
        summary_df = pd.DataFrame(summary_data)
        
        # Export to CSV
        summary_df.to_csv(filepath, index=False)
        print(f"✅ Market summary exported to: {filepath}")
        
        return filepath
    
    def export_all(self):
        """
        Export all available data formats
        """
        print(f"📊 Exporting all gamma exposure data for {self.symbol}")
        print("=" * 60)
        
        # Create export directory
        self.create_export_directory()
        
        exported_files = []
        
        # Export all formats
        exports = [
            ("Raw Gamma Data", self.export_raw_gamma_data),
            ("Gamma Matrix", self.export_gamma_matrix),
            ("Gamma by Strike", self.export_gamma_by_strike),
            ("Gamma by Expiration", self.export_gamma_by_expiration),
            ("Key Levels", self.export_key_levels),
            ("Market Summary", self.export_market_summary)
        ]
        
        for export_name, export_func in exports:
            try:
                print(f"\n📁 Exporting {export_name}...")
                filepath = export_func()
                if filepath:
                    exported_files.append(filepath)
            except Exception as e:
                print(f"❌ Failed to export {export_name}: {e}")
        
        print(f"\n" + "=" * 60)
        print(f"✅ Export completed!")
        print(f"📁 Export directory: {self.export_dir}")
        print(f"📄 Files exported: {len(exported_files)}")
        
        for filepath in exported_files:
            filename = os.path.basename(filepath)
            file_size = os.path.getsize(filepath) / 1024  # KB
            print(f"   📋 {filename} ({file_size:.1f} KB)")
        
        return exported_files

def create_gamma_exports(symbol, export_format="all"):
    """
    Standalone function to create gamma exposure exports
    
    Parameters:
    symbol (str): Stock symbol to analyze
    export_format (str): Format to export ("all", "matrix", "strike", "expiration", "raw", "levels", "summary")
    """
    print(f"🔥 Creating Gamma Exposure Exports for {symbol.upper()}")
    print("=" * 60)
    
    try:
        # Create analyzer and run analysis
        print("1️⃣ Initializing analyzer...")
        analyzer = GammaExposureAnalyzer(symbol)
        
        print("2️⃣ Getting current price...")
        analyzer.get_current_price()
        print(f"   Current Price: ${analyzer.current_price:.2f}")
        
        print("3️⃣ Fetching options data...")
        analyzer.get_options_data()
        
        print("4️⃣ Calculating gamma exposure...")
        analyzer.calculate_gamma_exposure()
        
        print("5️⃣ Creating CSV exporter...")
        exporter = GammaExposureCSVExporter(analyzer)
        
        print("6️⃣ Exporting data...")
        
        if export_format.lower() == "all":
            exported_files = exporter.export_all()
        elif export_format.lower() == "matrix":
            exporter.create_export_directory()
            exported_files = [exporter.export_gamma_matrix()]
        elif export_format.lower() == "strike":
            exporter.create_export_directory()
            exported_files = [exporter.export_gamma_by_strike()]
        elif export_format.lower() == "expiration":
            exporter.create_export_directory()
            exported_files = [exporter.export_gamma_by_expiration()]
        elif export_format.lower() == "raw":
            exporter.create_export_directory()
            exported_files = [exporter.export_raw_gamma_data()]
        elif export_format.lower() == "levels":
            exporter.create_export_directory()
            exported_files = [exporter.export_key_levels()]
        elif export_format.lower() == "summary":
            exporter.create_export_directory()
            exported_files = [exporter.export_market_summary()]
        else:
            print(f"❌ Unknown export format: {export_format}")
            return None
        
        print(f"\n✅ Export completed successfully!")
        return exported_files
        
    except Exception as e:
        print(f"❌ Export failed: {e}")
        import traceback
        traceback.print_exc()
        return None

def main():
    """
    Main function for interactive CSV export
    """
    print("📊 Gamma Exposure CSV Exporter")
    print("=" * 40)
    
    # Get symbol from user
    symbol = input("Enter symbol (e.g., SPY, AAPL): ").strip().upper()
    if not symbol:
        symbol = "SPY"
    
    print("\n📁 Export Options:")
    print("1. 📊 All formats")
    print("2. 🔥 Gamma Matrix (strikes vs expirations)")
    print("3. 📈 Gamma by Strike")
    print("4. ⏰ Gamma by Expiration")
    print("5. 📋 Raw Data")
    print("6. 🎯 Key Levels Only")
    print("7. 📄 Market Summary Only")
    
    choice = input("\nChoose export format (1-7): ").strip()
    
    format_map = {
        "1": "all",
        "2": "matrix",
        "3": "strike", 
        "4": "expiration",
        "5": "raw",
        "6": "levels",
        "7": "summary"
    }
    
    export_format = format_map.get(choice, "all")
    
    # Run export
    exported_files = create_gamma_exports(symbol, export_format)
    
    if exported_files:
        print(f"\n🎉 Success! Check the export directory for your CSV files.")
    else:
        print(f"\n❌ Export failed. Please try again.")

if __name__ == "__main__":
    main()