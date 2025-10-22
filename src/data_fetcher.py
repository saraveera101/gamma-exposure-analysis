"""
Options Data Fetcher Module
Fetches options chain data from various sources
"""

import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
from typing import Optional, List
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class OptionsDataFetcher:
    """Fetch options data for gamma exposure analysis"""
    
    def __init__(self, ticker: str):
        """
        Initialize options data fetcher
        
        Args:
            ticker: Stock ticker symbol (e.g., 'SPY', 'AAPL')
        """
        self.ticker = ticker.upper()
        self.yf_ticker = yf.Ticker(self.ticker)
    
    def get_current_price(self) -> Optional[float]:
        """
        Get current price of underlying
        
        Returns:
            Current price or None if failed
        """
        try:
            info = self.yf_ticker.info
            return info.get('currentPrice') or info.get('regularMarketPrice')
        except Exception as e:
            logger.error(f"Error fetching current price: {e}")
            return None
    
    def get_available_expirations(self) -> List[str]:
        """
        Get list of available expiration dates
        
        Returns:
            List of expiration dates as strings
        """
        try:
            return list(self.yf_ticker.options)
        except Exception as e:
            logger.error(f"Error fetching expirations: {e}")
            return []
    
    def fetch_options_chain(
        self, 
        expiration: Optional[str] = None,
        max_expirations: int = 3
    ) -> pd.DataFrame:
        """
        Fetch options chain data
        
        Args:
            expiration: Specific expiration date (YYYY-MM-DD) or None for nearest
            max_expirations: Maximum number of expirations to fetch if expiration is None
            
        Returns:
            DataFrame with options data
        """
        try:
            expirations = self.get_available_expirations()
            if not expirations:
                logger.warning("No expirations available")
                return pd.DataFrame()
            
            if expiration:
                expirations_to_fetch = [expiration] if expiration in expirations else []
            else:
                expirations_to_fetch = expirations[:max_expirations]
            
            all_options = []
            
            for exp_date in expirations_to_fetch:
                # Calculate days to expiration
                exp_datetime = datetime.strptime(exp_date, '%Y-%m-%d')
                today = datetime.now()
                dte = (exp_datetime - today).days
                
                # Fetch options chain
                opt_chain = self.yf_ticker.option_chain(exp_date)
                
                # Process calls
                calls = opt_chain.calls.copy()
                calls['type'] = 'call'
                calls['expiration'] = exp_date
                calls['dte'] = dte
                
                # Process puts
                puts = opt_chain.puts.copy()
                puts['type'] = 'put'
                puts['expiration'] = exp_date
                puts['dte'] = dte
                
                all_options.append(calls)
                all_options.append(puts)
            
            if not all_options:
                return pd.DataFrame()
            
            # Combine all options
            df = pd.concat(all_options, ignore_index=True)
            
            # Standardize column names
            df = df.rename(columns={
                'impliedVolatility': 'iv',
                'openInterest': 'oi',
                'lastPrice': 'last_price',
                'volume': 'volume'
            })
            
            # Filter and clean data
            df = df[df['iv'] > 0]  # Remove options with zero IV
            df = df[df['oi'] > 0]  # Remove options with zero open interest
            
            # Select relevant columns
            columns_to_keep = ['strike', 'dte', 'iv', 'oi', 'type', 
                             'expiration', 'last_price', 'volume']
            df = df[[col for col in columns_to_keep if col in df.columns]]
            
            return df
            
        except Exception as e:
            logger.error(f"Error fetching options chain: {e}")
            return pd.DataFrame()
    
    def get_ticker_info(self) -> dict:
        """
        Get ticker information
        
        Returns:
            Dictionary with ticker info
        """
        try:
            info = self.yf_ticker.info
            return {
                'name': info.get('longName', self.ticker),
                'sector': info.get('sector', 'N/A'),
                'current_price': self.get_current_price(),
                'market_cap': info.get('marketCap', 'N/A'),
                'avg_volume': info.get('averageVolume', 'N/A')
            }
        except Exception as e:
            logger.error(f"Error fetching ticker info: {e}")
            return {'name': self.ticker}
