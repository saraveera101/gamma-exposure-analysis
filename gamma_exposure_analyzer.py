"""
Gamma Exposure Analysis Tool
Based on HeatSeeker methodology for analyzing dealer positioning and gamma exposure
"""

import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
import warnings
from scipy import stats

warnings.filterwarnings('ignore')

class GammaExposureAnalyzer:
    """
    Main class for analyzing gamma exposure using options data from yfinance
    """
    
    def __init__(self, symbol, risk_free_rate=0.05):
        self.symbol = symbol.upper()
        self.risk_free_rate = risk_free_rate
        self.ticker = yf.Ticker(symbol)
        self.current_price = None
        self.options_data = {}
        self.gamma_exposure_data = None
        self.vanna_exposure_data = None
        
    def get_current_price(self):
        """Get current stock price"""
        try:
            info = self.ticker.info
            self.current_price = info.get('currentPrice', info.get('regularMarketPrice'))
            if self.current_price is None:
                # Fallback to recent price data
                hist = self.ticker.history(period="1d")
                self.current_price = hist['Close'].iloc[-1]
            return self.current_price
        except Exception as e:
            print(f"Error getting current price: {e}")
            return None
    
    def get_options_data(self):
        """Fetch all available options data"""
        try:
            # Get all expiration dates
            expirations = self.ticker.options
            self.options_data = {}
            
            print(f"Fetching options data for {self.symbol}...")
            print(f"Found {len(expirations)} expiration dates")
            
            for exp_date in expirations:
                try:
                    option_chain = self.ticker.option_chain(exp_date)
                    
                    # Process calls
                    calls = option_chain.calls.copy()
                    calls['type'] = 'call'
                    calls['expiration'] = exp_date
                    
                    # Process puts
                    puts = option_chain.puts.copy()
                    puts['type'] = 'put'
                    puts['expiration'] = exp_date
                    
                    # Combine calls and puts
                    all_options = pd.concat([calls, puts], ignore_index=True)
                    
                    # Calculate days to expiration
                    exp_datetime = pd.to_datetime(exp_date)
                    current_datetime = pd.to_datetime(datetime.now().date())
                    days_to_exp = (exp_datetime - current_datetime).days
                    all_options['days_to_expiration'] = days_to_exp
                    all_options['time_to_expiration'] = days_to_exp / 365.0
                    
                    self.options_data[exp_date] = all_options
                    print(f"Processed {exp_date}: {len(all_options)} options")
                    
                except Exception as e:
                    print(f"Error processing {exp_date}: {e}")
                    continue
                    
            return self.options_data
            
        except Exception as e:
            print(f"Error fetching options data: {e}")
            return None
    
    def black_scholes_greeks(self, S, K, T, r, sigma, option_type='call'):
        """
        Calculate Black-Scholes Greeks
        S: Current stock price
        K: Strike price
        T: Time to expiration (in years)
        r: Risk-free rate
        sigma: Implied volatility
        """
        if T <= 0 or sigma <= 0:
            return {'delta': 0, 'gamma': 0, 'vanna': 0, 'charm': 0}
        
        try:
            d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
            d2 = d1 - sigma * np.sqrt(T)
            
            # Calculate Greeks
            if option_type == 'call':
                delta = stats.norm.cdf(d1)
                charm = -stats.norm.pdf(d1) * (2 * r * T - d2 * sigma * np.sqrt(T)) / (2 * T * sigma * np.sqrt(T))
            else:  # put
                delta = stats.norm.cdf(d1) - 1
                charm = -stats.norm.pdf(d1) * (2 * r * T - d2 * sigma * np.sqrt(T)) / (2 * T * sigma * np.sqrt(T))
            
            gamma = stats.norm.pdf(d1) / (S * sigma * np.sqrt(T))
            vanna = -stats.norm.pdf(d1) * d2 / sigma
            
            return {'delta': delta, 'gamma': gamma, 'vanna': vanna, 'charm': charm}
            
        except Exception as e:
            print(f"Error calculating Greeks: {e}")
            return {'delta': 0, 'gamma': 0, 'vanna': 0, 'charm': 0}
    
    def calculate_gamma_exposure(self):
        """
        Calculate gamma exposure for all strikes and expirations
        Based on the formula: Gamma Exposure = Open Interest * Gamma * 100 * S^2 * 0.01
        """
        if not self.options_data or self.current_price is None:
            print("No options data or current price available")
            return None
        
        gamma_exposure_list = []
        total_options_processed = 0
        valid_options_count = 0
        
        for exp_date, options_df in self.options_data.items():
            exp_options_processed = 0
            exp_valid_options = 0
            
            for _, option in options_df.iterrows():
                total_options_processed += 1
                exp_options_processed += 1
                
                try:
                    # Skip options with missing data
                    if pd.isna(option['openInterest']) or pd.isna(option['impliedVolatility']):
                        continue
                    
                    if option['openInterest'] == 0:
                        continue
                    
                    if option['impliedVolatility'] <= 0:
                        continue
                    
                    # Calculate Greeks
                    greeks = self.black_scholes_greeks(
                        S=self.current_price,
                        K=option['strike'],
                        T=option['time_to_expiration'],
                        r=self.risk_free_rate,
                        sigma=option['impliedVolatility'],
                        option_type=option['type']
                    )
                    
                    # Calculate dealer gamma exposure
                    # Dealers are short gamma when they sell options
                    # For calls: negative gamma exposure (dealers short)
                    # For puts: positive gamma exposure (dealers long puts to hedge)
                    if option['type'] == 'call':
                        dealer_gamma_exposure = -option['openInterest'] * greeks['gamma'] * 100 * self.current_price ** 2 * 0.01
                    else:  # puts
                        dealer_gamma_exposure = option['openInterest'] * greeks['gamma'] * 100 * self.current_price ** 2 * 0.01
                    
                    # Calculate vanna exposure
                    dealer_vanna_exposure = -option['openInterest'] * greeks['vanna'] * 100 * self.current_price * 0.01
                    
                    # Calculate charm exposure
                    dealer_charm_exposure = -option['openInterest'] * greeks['charm'] * 100 * self.current_price * 0.01
                    
                    gamma_exposure_list.append({
                        'expiration': exp_date,
                        'days_to_expiration': option['days_to_expiration'],
                        'strike': option['strike'],
                        'type': option['type'],
                        'open_interest': option['openInterest'],
                        'implied_volatility': option['impliedVolatility'],
                        'delta': greeks['delta'],
                        'gamma': greeks['gamma'],
                        'vanna': greeks['vanna'],
                        'charm': greeks['charm'],
                        'gamma_exposure': dealer_gamma_exposure,
                        'vanna_exposure': dealer_vanna_exposure,
                        'charm_exposure': dealer_charm_exposure,
                        'last_price': option.get('lastPrice', 0),
                        'volume': option.get('volume', 0)
                    })
                    
                    valid_options_count += 1
                    exp_valid_options += 1
                    
                except Exception as e:
                    continue
            
            print(f"   {exp_date}: {exp_valid_options}/{exp_options_processed} valid options")
        
        self.gamma_exposure_data = pd.DataFrame(gamma_exposure_list)
        
        if len(self.gamma_exposure_data) > 0:
            total_gamma = self.gamma_exposure_data['gamma_exposure'].sum()
            non_zero_gamma = (self.gamma_exposure_data['gamma_exposure'] != 0).sum()
            print(f"Calculated gamma exposure for {len(self.gamma_exposure_data)} options")
            print(f"Valid options: {valid_options_count}/{total_options_processed}")
            print(f"Non-zero gamma exposures: {non_zero_gamma}")
            print(f"Total net gamma exposure: ${total_gamma:,.0f}")
            return self.gamma_exposure_data
        else:
            print("No valid gamma exposure data calculated")
            print(f"Processed {total_options_processed} total options, {valid_options_count} were valid")
            return None
    
    def aggregate_gamma_by_strike(self):
        """
        Aggregate gamma exposure by strike price across all expirations
        """
        if self.gamma_exposure_data is None:
            return None
        
        # Aggregate by strike
        gamma_by_strike = self.gamma_exposure_data.groupby('strike').agg({
            'gamma_exposure': 'sum',
            'vanna_exposure': 'sum',
            'open_interest': 'sum'
        }).reset_index()
        
        # Sort by strike
        gamma_by_strike = gamma_by_strike.sort_values('strike')
        
        # Identify king nodes (largest absolute gamma exposure)
        gamma_by_strike['abs_gamma_exposure'] = abs(gamma_by_strike['gamma_exposure'])
        king_node_idx = gamma_by_strike['abs_gamma_exposure'].idxmax()
        gamma_by_strike['is_king_node'] = False
        gamma_by_strike.loc[king_node_idx, 'is_king_node'] = True
        
        return gamma_by_strike
    
    def aggregate_gamma_by_expiration(self):
        """
        Create gamma exposure matrix by strike and expiration (like in the images)
        """
        if self.gamma_exposure_data is None:
            return None
        
        # Create pivot table
        gamma_matrix = self.gamma_exposure_data.pivot_table(
            index='strike',
            columns='expiration',
            values='gamma_exposure',
            aggfunc='sum',
            fill_value=0
        )
        
        # Sort strikes
        gamma_matrix = gamma_matrix.sort_index()
        
        # Sort columns by expiration date (correctly use columns parameter)
        gamma_matrix = gamma_matrix.reindex(columns=sorted(gamma_matrix.columns))
        
        return gamma_matrix

    def aggregate_vanna_by_expiration(self):
        """
        Create vanna exposure matrix by strike and expiration
        """
        if self.gamma_exposure_data is None:
            return None
        
        # Create pivot table
        vanna_matrix = self.gamma_exposure_data.pivot_table(
            index='strike',
            columns='expiration',
            values='vanna_exposure',
            aggfunc='sum',
            fill_value=0
        )
        
        # Sort strikes
        vanna_matrix = vanna_matrix.sort_index()
        
        # Sort columns by expiration date
        vanna_matrix = vanna_matrix.reindex(columns=sorted(vanna_matrix.columns))
        
        return vanna_matrix

    def aggregate_charm_by_expiration(self):
        """
        Create charm exposure matrix by strike and expiration
        """
        if self.gamma_exposure_data is None:
            return None
        
        # Create pivot table
        charm_matrix = self.gamma_exposure_data.pivot_table(
            index='strike',
            columns='expiration',
            values='charm_exposure',
            aggfunc='sum',
            fill_value=0
        )
        
        # Sort strikes
        charm_matrix = charm_matrix.sort_index()
        
        # Sort columns by expiration date
        charm_matrix = charm_matrix.reindex(columns=sorted(charm_matrix.columns))
        
        return charm_matrix

    def identify_gamma_levels(self):
        """
        Identify key gamma levels and their characteristics
        """
        gamma_by_strike = self.aggregate_gamma_by_strike()
        if gamma_by_strike is None:
            return None
        
        # Identify positive and negative nodes
        positive_nodes = gamma_by_strike[gamma_by_strike['gamma_exposure'] > 0].copy()
        negative_nodes = gamma_by_strike[gamma_by_strike['gamma_exposure'] < 0].copy()
        
        # Find largest nodes
        if len(positive_nodes) > 0:
            largest_positive = positive_nodes.loc[positive_nodes['gamma_exposure'].idxmax()]
        else:
            largest_positive = None
            
        if len(negative_nodes) > 0:
            largest_negative = negative_nodes.loc[negative_nodes['abs_gamma_exposure'].idxmax()]
        else:
            largest_negative = None
        
        # Identify support and resistance levels
        current_price = self.current_price
        
        # Find nearest gamma levels
        above_current = gamma_by_strike[gamma_by_strike['strike'] > current_price]
        below_current = gamma_by_strike[gamma_by_strike['strike'] < current_price]
        
        resistance_levels = []
        support_levels = []
        
        if len(above_current) > 0:
            # Find significant gamma levels above current price
            significant_above = above_current[above_current['abs_gamma_exposure'] > above_current['abs_gamma_exposure'].quantile(0.7)]
            resistance_levels = significant_above.nlargest(3, 'abs_gamma_exposure')['strike'].tolist()
        
        if len(below_current) > 0:
            # Find significant gamma levels below current price
            significant_below = below_current[below_current['abs_gamma_exposure'] > below_current['abs_gamma_exposure'].quantile(0.7)]
            support_levels = significant_below.nlargest(3, 'abs_gamma_exposure')['strike'].tolist()
        
        return {
            'positive_nodes': positive_nodes,
            'negative_nodes': negative_nodes,
            'largest_positive': largest_positive,
            'largest_negative': largest_negative,
            'resistance_levels': resistance_levels,
            'support_levels': support_levels,
            'king_node': gamma_by_strike[gamma_by_strike['is_king_node']].iloc[0] if len(gamma_by_strike) > 0 else None
        }
    
    def plot_gamma_exposure_heatmap(self):
        """
        Create a heatmap similar to the ones in the images
        """
        gamma_matrix = self.aggregate_gamma_by_expiration()
        if gamma_matrix is None:
            print("No gamma matrix data available")
            return None
        
        # Create the plot
        plt.figure(figsize=(15, 10))
        
        # Create custom colormap (blue to purple for negative, green to yellow for positive)
        colors_negative = ['#4a0e4e', '#8e44ad', '#bb5eb5']  # purple shades
        colors_positive = ['#27ae60', '#f39c12', '#f1c40f']  # green to yellow
        
        # Normalize the data for better visualization
        vmin = gamma_matrix.min().min()
        vmax = gamma_matrix.max().max()
        
        # Create heatmap
        sns.heatmap(gamma_matrix, 
                   cmap='RdYlBu_r',  # Red-Yellow-Blue reversed
                   center=0,
                   annot=True, 
                   fmt='.0f',
                   cbar_kws={'label': 'Gamma Exposure ($)'})
        
        plt.title(f'{self.symbol} Gamma Exposure Heatmap\nCurrent Price: ${self.current_price:.2f}', 
                 fontsize=16, fontweight='bold')
        plt.xlabel('Expiration Date', fontsize=12)
        plt.ylabel('Strike Price', fontsize=12)
        
        # Add current price line
        current_price_position = None
        strikes = gamma_matrix.index.tolist()
        if strikes:
            # Find closest strike to current price
            current_price_position = min(range(len(strikes)), 
                                       key=lambda i: abs(strikes[i] - self.current_price))
            plt.axhline(y=current_price_position + 0.5, color='red', linewidth=3, 
                       label=f'Current Price: ${self.current_price:.2f}')
        
        plt.legend()
        plt.tight_layout()
        plt.show()
        
        return gamma_matrix
    
    def plot_gamma_profile(self):
        """
        Plot gamma exposure profile by strike price
        """
        gamma_by_strike = self.aggregate_gamma_by_strike()
        if gamma_by_strike is None:
            print("No gamma data available")
            return None
        
        plt.figure(figsize=(12, 8))
        
        # Create bar plot with colors based on positive/negative
        colors = ['green' if x > 0 else 'purple' for x in gamma_by_strike['gamma_exposure']]
        
        bars = plt.bar(gamma_by_strike['strike'], gamma_by_strike['gamma_exposure'], 
                      color=colors, alpha=0.7)
        
        # Highlight king node
        king_node = gamma_by_strike[gamma_by_strike['is_king_node']]
        if len(king_node) > 0:
            king_strike = king_node['strike'].iloc[0]
            king_gamma = king_node['gamma_exposure'].iloc[0]
            plt.bar(king_strike, king_gamma, color='gold', alpha=0.9, 
                   label=f'King Node: ${king_strike:.0f}')
        
        # Add current price line
        plt.axvline(x=self.current_price, color='red', linewidth=2, linestyle='--',
                   label=f'Current Price: ${self.current_price:.2f}')
        
        plt.title(f'{self.symbol} Gamma Exposure Profile', fontsize=16, fontweight='bold')
        plt.xlabel('Strike Price ($)', fontsize=12)
        plt.ylabel('Gamma Exposure ($)', fontsize=12)
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.show()
        
        return gamma_by_strike
    
    def analyze_market_sentiment(self):
        """
        Analyze overall market sentiment based on gamma exposure
        """
        gamma_by_strike = self.aggregate_gamma_by_strike()
        if gamma_by_strike is None:
            return None
        
        # Calculate net gamma exposure
        total_positive_gamma = gamma_by_strike[gamma_by_strike['gamma_exposure'] > 0]['gamma_exposure'].sum()
        total_negative_gamma = gamma_by_strike[gamma_by_strike['gamma_exposure'] < 0]['gamma_exposure'].sum()
        net_gamma = total_positive_gamma + total_negative_gamma
        
        # Analyze gamma around current price
        price_range = self.current_price * 0.05  # 5% range around current price
        near_money_options = gamma_by_strike[
            (gamma_by_strike['strike'] >= self.current_price - price_range) &
            (gamma_by_strike['strike'] <= self.current_price + price_range)
        ]
        
        near_money_gamma = near_money_options['gamma_exposure'].sum()
        
        # Determine market regime
        if net_gamma > 0 and near_money_gamma > 0:
            regime = "Positive Gamma Environment - Expect Lower Volatility"
            color = "🟡"  # Yellow
        elif net_gamma < 0 and near_money_gamma < 0:
            regime = "Negative Gamma Environment - Expect Higher Volatility"
            color = "🟣"  # Purple
        else:
            regime = "Mixed Gamma Environment - Moderate Volatility Expected"
            color = "⚪"  # White
        
        # Find gamma flip point (zero gamma level)
        gamma_flip_candidates = []
        for i in range(len(gamma_by_strike) - 1):
            current_gamma = gamma_by_strike.iloc[i]['gamma_exposure']
            next_gamma = gamma_by_strike.iloc[i + 1]['gamma_exposure']
            
            if (current_gamma > 0 and next_gamma < 0) or (current_gamma < 0 and next_gamma > 0):
                gamma_flip_candidates.append({
                    'strike': (gamma_by_strike.iloc[i]['strike'] + gamma_by_strike.iloc[i + 1]['strike']) / 2,
                    'transition': f"{gamma_by_strike.iloc[i]['strike']:.0f} to {gamma_by_strike.iloc[i + 1]['strike']:.0f}"
                })
        
        return {
            'regime': regime,
            'color': color,
            'net_gamma': net_gamma,
            'total_positive_gamma': total_positive_gamma,
            'total_negative_gamma': total_negative_gamma,
            'near_money_gamma': near_money_gamma,
            'gamma_flip_points': gamma_flip_candidates
        }
    
    def generate_trading_signals(self):
        """
        Generate trading signals based on gamma exposure analysis
        """
        sentiment = self.analyze_market_sentiment()
        levels = self.identify_gamma_levels()
        
        if sentiment is None or levels is None:
            return None
        
        signals = []
        
        # Current price relative to gamma levels
        current_price = self.current_price
        
        # Support and resistance signals
        if levels['resistance_levels']:
            nearest_resistance = min(levels['resistance_levels'], 
                                   key=lambda x: abs(x - current_price) if x > current_price else float('inf'))
            if nearest_resistance > current_price:
                distance_to_resistance = (nearest_resistance - current_price) / current_price * 100
                signals.append(f"📈 Resistance at ${nearest_resistance:.0f} ({distance_to_resistance:.1f}% above)")
        
        if levels['support_levels']:
            nearest_support = min(levels['support_levels'], 
                                key=lambda x: abs(x - current_price) if x < current_price else float('inf'))
            if nearest_support < current_price:
                distance_to_support = (current_price - nearest_support) / current_price * 100
                signals.append(f"📉 Support at ${nearest_support:.0f} ({distance_to_support:.1f}% below)")
        
        # King node analysis
        if levels['king_node'] is not None:
            king_strike = levels['king_node']['strike']
            king_gamma = levels['king_node']['gamma_exposure']
            distance_to_king = abs(king_strike - current_price) / current_price * 100
            
            if king_gamma > 0:
                signals.append(f"👑 King Node (Positive): ${king_strike:.0f} - Strong support/resistance level")
            else:
                signals.append(f"👑 King Node (Negative): ${king_strike:.0f} - Potential volatility catalyst")
        
        # Gamma flip signals
        if sentiment['gamma_flip_points']:
            for flip_point in sentiment['gamma_flip_points']:
                distance = abs(flip_point['strike'] - current_price) / current_price * 100
                if distance < 10:  # Within 10%
                    signals.append(f"⚡ Gamma Flip Zone: ${flip_point['strike']:.0f} - Major volatility shift possible")
        
        # Overall regime signal
        signals.append(f"{sentiment['color']} {sentiment['regime']}")
        
        return signals
    
    def run_complete_analysis(self):
        """
        Run the complete gamma exposure analysis
        """
        print(f"Starting Gamma Exposure Analysis for {self.symbol}")
        print("=" * 50)
        
        # Step 1: Get current price
        print("1. Getting current price...")
        current_price = self.get_current_price()
        if current_price is None:
            print("❌ Failed to get current price")
            return None
        print(f"✅ Current Price: ${current_price:.2f}")
        
        # Step 2: Fetch options data
        print("\n2. Fetching options data...")
        options_data = self.get_options_data()
        if not options_data:
            print("❌ Failed to fetch options data")
            return None
        print(f"✅ Fetched options for {len(options_data)} expiration dates")
        
        # Step 3: Calculate gamma exposure
        print("\n3. Calculating gamma exposure...")
        gamma_data = self.calculate_gamma_exposure()
        if gamma_data is None:
            print("❌ Failed to calculate gamma exposure")
            return None
        print(f"✅ Calculated gamma exposure for {len(gamma_data)} options")
        
        # Step 4: Analyze market sentiment
        print("\n4. Analyzing market sentiment...")
        sentiment = self.analyze_market_sentiment()
        if sentiment:
            print(f"✅ Market Regime: {sentiment['regime']}")
            print(f"   Net Gamma Exposure: ${sentiment['net_gamma']:,.0f}")
        
        # Step 5: Generate trading signals
        print("\n5. Generating trading signals...")
        signals = self.generate_trading_signals()
        if signals:
            print("✅ Trading Signals:")
            for signal in signals:
                print(f"   {signal}")
        
        # Step 6: Create visualizations
        print("\n6. Creating visualizations...")
        print("   📊 Gamma Profile Chart...")
        self.plot_gamma_profile()
        
        print("   🔥 Gamma Heatmap...")
        self.plot_gamma_exposure_heatmap()
        
        print("\n" + "=" * 50)
        print("✅ Analysis Complete!")
        
        return {
            'sentiment': sentiment,
            'signals': signals,
            'gamma_data': gamma_data,
            'current_price': current_price
        }

def main():
    """
    Main function to run the gamma exposure analysis
    """
    # Example usage
    symbol = input("Enter stock symbol (e.g., SPY, AAPL, TSLA): ").strip().upper()
    
    if not symbol:
        symbol = "SPY"  # Default to SPY
    
    print(f"Analyzing {symbol}...")
    
    # Create analyzer instance
    analyzer = GammaExposureAnalyzer(symbol)
    
    # Run complete analysis
    results = analyzer.run_complete_analysis()
    
    return results

if __name__ == "__main__":
    main()