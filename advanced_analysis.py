"""
Advanced Gamma Analysis Utilities
Additional features for enhanced gamma exposure analysis
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import yfinance as yf
from datetime import datetime, timedelta
import warnings

# Import plotly with error handling
try:
    import plotly.graph_objects as go
    from plotly.subplots import make_subplots
    PLOTLY_AVAILABLE = True
except ImportError:
    print("Warning: Plotly not installed. Interactive charts will be disabled.")
    PLOTLY_AVAILABLE = False

warnings.filterwarnings('ignore')

# Import the main analyzer class
from gamma_exposure_analyzer import GammaExposureAnalyzer

class AdvancedGammaAnalysis:
    """
    Advanced utilities for gamma exposure analysis
    """
    
    def __init__(self, analyzer):
        self.analyzer = analyzer
        self.symbol = analyzer.symbol
    
    def calculate_gex_profile_levels(self, num_levels=10):
        """
        Calculate key GEX profile levels for intraday trading
        """
        gamma_by_strike = self.analyzer.aggregate_gamma_by_strike()
        if gamma_by_strike is None:
            return None
        
        # Sort by absolute gamma exposure
        sorted_gamma = gamma_by_strike.sort_values('abs_gamma_exposure', ascending=False)
        
        # Get top levels
        key_levels = sorted_gamma.head(num_levels).copy()
        key_levels['level_type'] = key_levels['gamma_exposure'].apply(
            lambda x: 'Resistance/Support' if x > 0 else 'Volatility Catalyst'
        )
        
        # Add distance from current price
        current_price = self.analyzer.current_price
        key_levels['distance_pct'] = abs(key_levels['strike'] - current_price) / current_price * 100
        key_levels['direction'] = np.where(key_levels['strike'] > current_price, 'Above', 'Below')
        
        return key_levels.sort_values('distance_pct')
    
    def calculate_dealer_positioning(self):
        """
        Calculate overall dealer positioning analysis
        """
        if self.analyzer.gamma_exposure_data is None:
            return None
        
        data = self.analyzer.gamma_exposure_data
        current_price = self.analyzer.current_price
        
        # Separate calls and puts
        calls = data[data['type'] == 'call']
        puts = data[data['type'] == 'put']
        
        # Calculate dealer exposure by option type
        call_gamma_exposure = calls['gamma_exposure'].sum()
        put_gamma_exposure = puts['gamma_exposure'].sum()
        
        # ATM analysis (within 2% of current price)
        atm_range = current_price * 0.02
        atm_options = data[
            (data['strike'] >= current_price - atm_range) &
            (data['strike'] <= current_price + atm_range)
        ]
        
        atm_call_gamma = atm_options[atm_options['type'] == 'call']['gamma_exposure'].sum()
        atm_put_gamma = atm_options[atm_options['type'] == 'put']['gamma_exposure'].sum()
        
        # Calculate put/call ratio by gamma exposure
        pc_ratio_gamma = abs(put_gamma_exposure) / abs(call_gamma_exposure) if call_gamma_exposure != 0 else 0
        
        return {
            'call_gamma_exposure': call_gamma_exposure,
            'put_gamma_exposure': put_gamma_exposure,
            'net_gamma_exposure': call_gamma_exposure + put_gamma_exposure,
            'atm_call_gamma': atm_call_gamma,
            'atm_put_gamma': atm_put_gamma,
            'atm_net_gamma': atm_call_gamma + atm_put_gamma,
            'pc_ratio_gamma': pc_ratio_gamma
        }
    
    def identify_dealer_hedging_zones(self):
        """
        Identify zones where dealers will be actively hedging
        """
        gamma_by_strike = self.analyzer.aggregate_gamma_by_strike()
        if gamma_by_strike is None:
            return None
        
        current_price = self.analyzer.current_price
        
        # Define zones based on gamma exposure magnitude
        threshold_high = gamma_by_strike['abs_gamma_exposure'].quantile(0.8)
        threshold_medium = gamma_by_strike['abs_gamma_exposure'].quantile(0.6)
        
        zones = []
        
        for _, row in gamma_by_strike.iterrows():
            strike = row['strike']
            gamma_exp = row['gamma_exposure']
            abs_gamma_exp = row['abs_gamma_exposure']
            
            if abs_gamma_exp >= threshold_high:
                intensity = "High"
            elif abs_gamma_exp >= threshold_medium:
                intensity = "Medium"
            else:
                intensity = "Low"
            
            zone_type = "Support/Resistance" if gamma_exp > 0 else "Volatility Zone"
            
            zones.append({
                'strike': strike,
                'gamma_exposure': gamma_exp,
                'intensity': intensity,
                'zone_type': zone_type,
                'distance_from_spot': abs(strike - current_price),
                'distance_pct': abs(strike - current_price) / current_price * 100
            })
        
        return pd.DataFrame(zones).sort_values('distance_from_spot')
    
    def create_interactive_gamma_chart(self):
        """
        Create an interactive gamma exposure chart using Plotly
        """
        if not PLOTLY_AVAILABLE:
            print("❌ Plotly not available. Please install plotly to use interactive charts.")
            print("   Run: pip install plotly")
            return None
            
        gamma_by_strike = self.analyzer.aggregate_gamma_by_strike()
        if gamma_by_strike is None:
            return None
        
        current_price = self.analyzer.current_price
        
        # Create subplots
        fig = make_subplots(
            rows=2, cols=1,
            shared_xaxes=True,
            subplot_titles=('Gamma Exposure by Strike', 'Vanna Exposure by Strike'),
            vertical_spacing=0.1
        )
        
        # Colors based on positive/negative
        colors = ['green' if x > 0 else 'red' for x in gamma_by_strike['gamma_exposure']]
        vanna_colors = ['blue' if x > 0 else 'orange' for x in gamma_by_strike['vanna_exposure']]
        
        # Gamma exposure bars
        fig.add_trace(
            go.Bar(
                x=gamma_by_strike['strike'],
                y=gamma_by_strike['gamma_exposure'],
                name='Gamma Exposure',
                marker_color=colors,
                hovertemplate='Strike: $%{x}<br>Gamma Exposure: $%{y:,.0f}<extra></extra>'
            ),
            row=1, col=1
        )
        
        # Vanna exposure bars
        fig.add_trace(
            go.Bar(
                x=gamma_by_strike['strike'],
                y=gamma_by_strike['vanna_exposure'],
                name='Vanna Exposure',
                marker_color=vanna_colors,
                hovertemplate='Strike: $%{x}<br>Vanna Exposure: $%{y:,.0f}<extra></extra>'
            ),
            row=2, col=1
        )
        
        # Add current price line
        fig.add_vline(
            x=current_price,
            line_dash="dash",
            line_color="black",
            annotation_text=f"Current Price: ${current_price:.2f}",
            annotation_position="top"
        )
        
        # Highlight king node
        king_node = gamma_by_strike[gamma_by_strike['is_king_node']]
        if len(king_node) > 0:
            king_strike = king_node['strike'].iloc[0]
            fig.add_vline(
                x=king_strike,
                line_dash="dot",
                line_color="gold",
                annotation_text=f"King Node: ${king_strike:.0f}",
                annotation_position="bottom"
            )
        
        # Update layout
        fig.update_layout(
            title=f'{self.symbol} Interactive Gamma & Vanna Exposure',
            height=800,
            showlegend=True
        )
        
        fig.update_xaxes(title_text="Strike Price", row=2, col=1)
        fig.update_yaxes(title_text="Gamma Exposure ($)", row=1, col=1)
        fig.update_yaxes(title_text="Vanna Exposure ($)", row=2, col=1)
        
        fig.show()
        return fig
    
    def calculate_gamma_flip_scenarios(self, price_moves=[-0.05, -0.03, -0.01, 0.01, 0.03, 0.05]):
        """
        Calculate how gamma exposure changes with different price scenarios
        """
        if self.analyzer.gamma_exposure_data is None:
            return None
        
        current_price = self.analyzer.current_price
        scenarios = []
        
        for move in price_moves:
            new_price = current_price * (1 + move)
            
            # Recalculate gamma exposure at new price
            scenario_gamma = 0
            for _, option in self.analyzer.gamma_exposure_data.iterrows():
                greeks = self.analyzer.black_scholes_greeks(
                    S=new_price,
                    K=option['strike'],
                    T=option['time_to_expiration'],
                    r=self.analyzer.risk_free_rate,
                    sigma=option['implied_volatility'],
                    option_type=option['type']
                )
                
                # Calculate dealer gamma exposure at new price
                if option['type'] == 'call':
                    dealer_gamma = -option['open_interest'] * greeks['gamma'] * 100 * new_price ** 2 * 0.01
                else:
                    dealer_gamma = option['open_interest'] * greeks['gamma'] * 100 * new_price ** 2 * 0.01
                
                scenario_gamma += dealer_gamma
            
            scenarios.append({
                'price_move_pct': move * 100,
                'new_price': new_price,
                'net_gamma_exposure': scenario_gamma
            })
        
        return pd.DataFrame(scenarios)
    
    def analyze_expiration_impact(self):
        """
        Analyze how gamma exposure changes as expiration approaches
        """
        if self.analyzer.gamma_exposure_data is None:
            return None
        
        # Group by expiration date
        exp_analysis = self.analyzer.gamma_exposure_data.groupby('expiration').agg({
            'gamma_exposure': 'sum',
            'vanna_exposure': 'sum',
            'days_to_expiration': 'first',
            'open_interest': 'sum'
        }).reset_index()
        
        # Sort by days to expiration
        exp_analysis = exp_analysis.sort_values('days_to_expiration')
        
        # Calculate impact scores
        exp_analysis['gamma_impact_score'] = abs(exp_analysis['gamma_exposure']) / exp_analysis['days_to_expiration'].replace(0, 1)
        
        return exp_analysis
    
    def generate_intraday_levels_report(self):
        """
        Generate a comprehensive report of key levels for intraday trading
        """
        current_price = self.analyzer.current_price
        levels = self.calculate_gex_profile_levels()
        zones = self.identify_dealer_hedging_zones()
        positioning = self.calculate_dealer_positioning()
        
        if levels is None:
            return None
        
        report = {
            'timestamp': datetime.now(),
            'symbol': self.symbol,
            'current_price': current_price,
            'market_regime': self.analyzer.analyze_market_sentiment()['regime'],
            'key_levels': levels,
            'hedging_zones': zones,
            'dealer_positioning': positioning
        }
        
        return report
    
    def plot_comprehensive_analysis(self):
        """
        Create a comprehensive multi-panel analysis chart
        """
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(20, 15))
        
        # 1. Gamma Profile
        gamma_by_strike = self.analyzer.aggregate_gamma_by_strike()
        if gamma_by_strike is not None:
            colors = ['green' if x > 0 else 'red' for x in gamma_by_strike['gamma_exposure']]
            ax1.bar(gamma_by_strike['strike'], gamma_by_strike['gamma_exposure'], color=colors, alpha=0.7)
            ax1.axvline(x=self.analyzer.current_price, color='black', linestyle='--', linewidth=2)
            ax1.set_title('Gamma Exposure Profile')
            ax1.set_xlabel('Strike Price')
            ax1.set_ylabel('Gamma Exposure ($)')
            ax1.grid(True, alpha=0.3)
        
        # 2. Vanna Profile
        if gamma_by_strike is not None:
            vanna_colors = ['blue' if x > 0 else 'orange' for x in gamma_by_strike['vanna_exposure']]
            ax2.bar(gamma_by_strike['strike'], gamma_by_strike['vanna_exposure'], color=vanna_colors, alpha=0.7)
            ax2.axvline(x=self.analyzer.current_price, color='black', linestyle='--', linewidth=2)
            ax2.set_title('Vanna Exposure Profile')
            ax2.set_xlabel('Strike Price')
            ax2.set_ylabel('Vanna Exposure ($)')
            ax2.grid(True, alpha=0.3)
        
        # 3. Open Interest by Strike
        if gamma_by_strike is not None:
            ax3.bar(gamma_by_strike['strike'], gamma_by_strike['open_interest'], color='gray', alpha=0.7)
            ax3.axvline(x=self.analyzer.current_price, color='black', linestyle='--', linewidth=2)
            ax3.set_title('Open Interest by Strike')
            ax3.set_xlabel('Strike Price')
            ax3.set_ylabel('Open Interest')
            ax3.grid(True, alpha=0.3)
        
        # 4. Expiration Analysis
        exp_analysis = self.analyze_expiration_impact()
        if exp_analysis is not None:
            ax4.bar(range(len(exp_analysis)), exp_analysis['gamma_exposure'], 
                   color=['red' if x < 0 else 'green' for x in exp_analysis['gamma_exposure']], alpha=0.7)
            ax4.set_title('Gamma Exposure by Expiration')
            ax4.set_xlabel('Expiration (Days to Exp)')
            ax4.set_ylabel('Gamma Exposure ($)')
            ax4.set_xticks(range(len(exp_analysis)))
            ax4.set_xticklabels([f"{int(x)}d" for x in exp_analysis['days_to_expiration']], rotation=45)
            ax4.grid(True, alpha=0.3)
        
        plt.suptitle(f'{self.symbol} Comprehensive Gamma Analysis - ${self.analyzer.current_price:.2f}', 
                    fontsize=16, fontweight='bold')
        plt.tight_layout()
        plt.show()

def create_gamma_scanner(symbols_list):
    """
    Scan multiple symbols for gamma exposure analysis
    """
    results = {}
    
    print("Starting Gamma Scanner...")
    print("=" * 50)
    
    for symbol in symbols_list:
        try:
            print(f"\nScanning {symbol}...")
            analyzer = GammaExposureAnalyzer(symbol)
            
            # Quick analysis
            analyzer.get_current_price()
            analyzer.get_options_data()
            analyzer.calculate_gamma_exposure()
            
            sentiment = analyzer.analyze_market_sentiment()
            levels = analyzer.identify_gamma_levels()
            
            if sentiment and levels:
                results[symbol] = {
                    'current_price': analyzer.current_price,
                    'regime': sentiment['regime'],
                    'net_gamma': sentiment['net_gamma'],
                    'king_node': levels['king_node']['strike'] if levels['king_node'] is not None else None
                }
                print(f"✅ {symbol}: {sentiment['regime']}")
            else:
                print(f"❌ {symbol}: Failed to analyze")
                
        except Exception as e:
            print(f"❌ {symbol}: Error - {e}")
            continue
    
    print("\n" + "=" * 50)
    print("Scanner Results:")
    
    for symbol, data in results.items():
        print(f"{symbol}: {data['regime']} | Price: ${data['current_price']:.2f} | King Node: ${data['king_node']:.0f}")
    
    return results

# Example usage functions
def quick_spy_analysis():
    """Quick SPY analysis"""
    analyzer = GammaExposureAnalyzer("SPY")
    return analyzer.run_complete_analysis()

def quick_qqq_analysis():
    """Quick QQQ analysis"""
    analyzer = GammaExposureAnalyzer("QQQ")
    return analyzer.run_complete_analysis()

def scan_major_etfs():
    """Scan major ETFs for gamma exposure"""
    etfs = ["SPY", "QQQ", "IWM", "DIA", "VIX"]
    return create_gamma_scanner(etfs)