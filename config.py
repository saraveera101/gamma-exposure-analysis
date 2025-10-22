"""
Configuration settings for Gamma Exposure Analysis Tool
"""

# Default risk-free rate (adjust based on current rates)
DEFAULT_RISK_FREE_RATE = 0.05

# Analysis settings
DEFAULT_GAMMA_THRESHOLD = 1000  # Minimum gamma exposure to consider significant
DEFAULT_KING_NODE_THRESHOLD = 0.8  # Percentile for identifying king nodes

# Chart settings
CHART_STYLE = 'seaborn-v0_8'  # matplotlib style
FIGURE_SIZE = (12, 8)  # Default figure size
DPI = 100  # Chart resolution

# Color schemes
COLORS = {
    'positive_gamma': 'green',
    'negative_gamma': 'red', 
    'positive_vanna': 'blue',
    'negative_vanna': 'orange',
    'current_price': 'black',
    'king_node': 'gold',
    'support': 'green',
    'resistance': 'red'
}

# Symbol lists for quick analysis
POPULAR_SYMBOLS = {
    'ETFs': ['SPY', 'QQQ', 'IWM', 'DIA', 'VIX', 'GLD', 'TLT'],
    'Mega_Caps': ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA', 'META', 'NVDA'],
    'High_Beta': ['TSLA', 'AMD', 'NFLX', 'ROKU', 'ZOOM', 'PELOTON'],
    'Financials': ['JPM', 'BAC', 'GS', 'WFC', 'C', 'MS'],
    'Tech': ['AAPL', 'MSFT', 'GOOGL', 'META', 'NFLX', 'CRM', 'ORCL']
}

# Market hours (for data quality considerations)
MARKET_HOURS = {
    'open': '09:30',  # EST
    'close': '16:00',  # EST
    'timezone': 'US/Eastern'
}

# Options data filters
OPTIONS_FILTERS = {
    'min_open_interest': 10,  # Minimum open interest to consider
    'min_volume': 1,  # Minimum daily volume
    'max_days_to_expiry': 365,  # Maximum days to expiry to include
    'min_iv': 0.01,  # Minimum implied volatility
    'max_iv': 5.0   # Maximum implied volatility
}

# Analysis ranges
ANALYSIS_RANGES = {
    'atm_range_pct': 0.02,  # 2% range for ATM analysis
    'support_resistance_range_pct': 0.10,  # 10% range for S/R levels
    'king_node_range_pct': 0.05  # 5% range around king nodes
}

# Display settings
DISPLAY_SETTINGS = {
    'max_levels_to_show': 10,  # Maximum levels to display in reports
    'decimal_places': 2,  # Decimal places for price display
    'currency_symbol': '$',  # Currency symbol for display
    'percentage_format': '.1f'  # Format for percentage display
}

# Performance settings
PERFORMANCE = {
    'max_concurrent_requests': 5,  # For multi-symbol analysis
    'request_delay': 0.1,  # Delay between API requests (seconds)
    'cache_timeout': 300,  # Cache timeout in seconds
    'max_options_per_expiry': 1000  # Maximum options to process per expiry
}