"""
Gamma Exposure Calculator Module
Calculates gamma exposure for options chains
"""

import numpy as np
import pandas as pd
from scipy.stats import norm
from typing import Dict, Tuple, Optional


class GammaCalculator:
    """Calculate gamma exposure metrics for options"""
    
    def __init__(self, spot_price: float, risk_free_rate: float = 0.05):
        """
        Initialize gamma calculator
        
        Args:
            spot_price: Current price of underlying asset
            risk_free_rate: Risk-free interest rate (default 5%)
        """
        self.spot_price = spot_price
        self.risk_free_rate = risk_free_rate
    
    def black_scholes_gamma(
        self, 
        strike: float, 
        time_to_expiry: float, 
        volatility: float,
        option_type: str = 'call'
    ) -> float:
        """
        Calculate Black-Scholes gamma
        
        Args:
            strike: Strike price
            time_to_expiry: Time to expiration in years
            volatility: Implied volatility (annualized)
            option_type: 'call' or 'put'
            
        Returns:
            Gamma value
        """
        if time_to_expiry <= 0 or volatility <= 0:
            return 0.0
        
        d1 = (np.log(self.spot_price / strike) + 
              (self.risk_free_rate + 0.5 * volatility**2) * time_to_expiry) / \
             (volatility * np.sqrt(time_to_expiry))
        
        gamma = norm.pdf(d1) / (self.spot_price * volatility * np.sqrt(time_to_expiry))
        return gamma
    
    def calculate_gamma_exposure(
        self,
        options_df: pd.DataFrame,
        notional_multiplier: float = 100
    ) -> pd.DataFrame:
        """
        Calculate gamma exposure for options chain
        
        Args:
            options_df: DataFrame with columns ['strike', 'dte', 'iv', 'oi', 'type']
                       where oi is open interest
            notional_multiplier: Multiplier for contract size (default 100 for stocks)
            
        Returns:
            DataFrame with gamma exposure by strike
        """
        results = []
        
        for _, row in options_df.iterrows():
            gamma = self.black_scholes_gamma(
                strike=row['strike'],
                time_to_expiry=row['dte'] / 365.0,
                volatility=row['iv'],
                option_type=row['type']
            )
            
            # Gamma exposure = Gamma * Open Interest * Notional * Spot^2
            # Market makers are short gamma for net call buying
            sign = 1 if row['type'] == 'put' else -1
            gamma_exposure = sign * gamma * row['oi'] * notional_multiplier * self.spot_price**2
            
            results.append({
                'strike': row['strike'],
                'gamma': gamma,
                'gamma_exposure': gamma_exposure,
                'open_interest': row['oi'],
                'type': row['type']
            })
        
        return pd.DataFrame(results)
    
    def aggregate_gamma_by_strike(self, gamma_df: pd.DataFrame) -> pd.DataFrame:
        """
        Aggregate gamma exposure by strike price
        
        Args:
            gamma_df: DataFrame from calculate_gamma_exposure
            
        Returns:
            Aggregated DataFrame by strike
        """
        aggregated = gamma_df.groupby('strike').agg({
            'gamma_exposure': 'sum',
            'open_interest': 'sum'
        }).reset_index()
        
        return aggregated.sort_values('strike')
    
    def find_gamma_levels(self, aggregated_df: pd.DataFrame) -> Dict[str, float]:
        """
        Find key gamma exposure levels
        
        Args:
            aggregated_df: Aggregated gamma exposure DataFrame
            
        Returns:
            Dictionary with key levels (zero gamma, max positive, max negative)
        """
        if aggregated_df.empty:
            return {}
        
        # Find zero gamma crossover (gamma flip point)
        zero_gamma_idx = (aggregated_df['gamma_exposure'].abs()).idxmin()
        zero_gamma = aggregated_df.loc[zero_gamma_idx, 'strike']
        
        # Find max positive and negative gamma exposure
        max_pos_idx = aggregated_df['gamma_exposure'].idxmax()
        max_neg_idx = aggregated_df['gamma_exposure'].idxmin()
        
        return {
            'zero_gamma_level': zero_gamma,
            'max_positive_strike': aggregated_df.loc[max_pos_idx, 'strike'],
            'max_positive_gex': aggregated_df.loc[max_pos_idx, 'gamma_exposure'],
            'max_negative_strike': aggregated_df.loc[max_neg_idx, 'strike'],
            'max_negative_gex': aggregated_df.loc[max_neg_idx, 'gamma_exposure'],
            'total_gamma_exposure': aggregated_df['gamma_exposure'].sum()
        }
