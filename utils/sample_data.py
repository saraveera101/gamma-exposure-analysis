"""
Sample data generator for demo mode
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta


def generate_sample_options_data(ticker: str, spot_price: float, num_strikes: int = 20) -> pd.DataFrame:
    """
    Generate sample options data for demonstration
    
    Args:
        ticker: Ticker symbol
        spot_price: Current price of underlying
        num_strikes: Number of strikes to generate
        
    Returns:
        DataFrame with sample options data
    """
    np.random.seed(42)  # For reproducibility
    
    # Generate strikes around the spot price
    strike_range = spot_price * 0.2  # +/- 20% from spot
    strikes = np.linspace(spot_price - strike_range, spot_price + strike_range, num_strikes)
    
    options_data = []
    
    # Generate data for 3 expirations
    dtes = [7, 30, 60]  # Days to expiration
    
    for dte in dtes:
        for strike in strikes:
            # Distance from spot (in %)
            moneyness = (strike - spot_price) / spot_price
            
            # Generate realistic IV smile (higher IV for OTM options)
            base_iv = 0.20
            iv_call = base_iv + abs(moneyness) * 0.3 if moneyness > 0 else base_iv + abs(moneyness) * 0.2
            iv_put = base_iv + abs(moneyness) * 0.3 if moneyness < 0 else base_iv + abs(moneyness) * 0.2
            
            # Generate open interest (higher near the money)
            atm_factor = np.exp(-10 * moneyness**2)
            base_oi = 5000 * atm_factor * (60 / dte)  # More OI for near-term
            
            # Add some randomness
            oi_call = int(base_oi * np.random.uniform(0.8, 1.2))
            oi_put = int(base_oi * np.random.uniform(0.9, 1.3))
            
            # Calls
            options_data.append({
                'strike': round(strike, 2),
                'dte': dte,
                'iv': iv_call,
                'oi': max(100, oi_call),  # Minimum 100 OI
                'type': 'call',
                'expiration': (datetime.now() + timedelta(days=dte)).strftime('%Y-%m-%d'),
                'last_price': max(0.01, (spot_price - strike) + spot_price * iv_call * np.sqrt(dte/365)),
                'volume': int(max(10, oi_call * np.random.uniform(0.05, 0.15)))
            })
            
            # Puts
            options_data.append({
                'strike': round(strike, 2),
                'dte': dte,
                'iv': iv_put,
                'oi': max(100, oi_put),
                'type': 'put',
                'expiration': (datetime.now() + timedelta(days=dte)).strftime('%Y-%m-%d'),
                'last_price': max(0.01, (strike - spot_price) + spot_price * iv_put * np.sqrt(dte/365)),
                'volume': int(max(10, oi_put * np.random.uniform(0.05, 0.15)))
            })
    
    return pd.DataFrame(options_data)


def get_sample_ticker_info(ticker: str, spot_price: float) -> dict:
    """
    Generate sample ticker information
    
    Args:
        ticker: Ticker symbol
        spot_price: Current price
        
    Returns:
        Dictionary with ticker info
    """
    ticker_info = {
        'SPY': {
            'name': 'SPDR S&P 500 ETF Trust',
            'sector': 'ETF',
            'market_cap': '500B+',
            'avg_volume': '50M+'
        },
        'AAPL': {
            'name': 'Apple Inc.',
            'sector': 'Technology',
            'market_cap': '3T+',
            'avg_volume': '50M+'
        },
        'TSLA': {
            'name': 'Tesla, Inc.',
            'sector': 'Automotive',
            'market_cap': '800B+',
            'avg_volume': '100M+'
        },
        'QQQ': {
            'name': 'Invesco QQQ Trust',
            'sector': 'ETF',
            'market_cap': '200B+',
            'avg_volume': '30M+'
        },
        'NVDA': {
            'name': 'NVIDIA Corporation',
            'sector': 'Technology',
            'market_cap': '1T+',
            'avg_volume': '200M+'
        }
    }
    
    default_info = {
        'name': f'{ticker} (Sample Data)',
        'sector': 'N/A',
        'market_cap': 'N/A',
        'avg_volume': 'N/A'
    }
    
    info = ticker_info.get(ticker, default_info)
    info['current_price'] = spot_price
    
    return info


# Sample spot prices for common tickers
SAMPLE_SPOT_PRICES = {
    'SPY': 450.00,
    'QQQ': 380.00,
    'AAPL': 175.00,
    'TSLA': 250.00,
    'NVDA': 500.00,
    'IWM': 200.00,
    'DIA': 350.00,
    'AMZN': 145.00,
    'MSFT': 375.00,
    'GOOGL': 140.00
}
