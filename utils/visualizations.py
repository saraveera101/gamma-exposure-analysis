"""
Visualization Utilities for Gamma Exposure Analysis
"""

import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from typing import Optional


def create_gamma_exposure_chart(
    aggregated_df: pd.DataFrame,
    current_price: float,
    ticker: str
) -> go.Figure:
    """
    Create interactive gamma exposure bar chart
    
    Args:
        aggregated_df: DataFrame with strike and gamma_exposure columns
        current_price: Current price of underlying
        ticker: Ticker symbol
        
    Returns:
        Plotly figure
    """
    fig = go.Figure()
    
    # Color bars based on positive/negative exposure
    colors = ['green' if x >= 0 else 'red' for x in aggregated_df['gamma_exposure']]
    
    fig.add_trace(go.Bar(
        x=aggregated_df['strike'],
        y=aggregated_df['gamma_exposure'],
        marker_color=colors,
        name='Gamma Exposure',
        hovertemplate='<b>Strike:</b> $%{x:.2f}<br>' +
                      '<b>Gamma Exposure:</b> %{y:,.0f}<br>' +
                      '<extra></extra>'
    ))
    
    # Add current price line
    fig.add_vline(
        x=current_price,
        line_dash="dash",
        line_color="blue",
        annotation_text=f"Current Price: ${current_price:.2f}",
        annotation_position="top"
    )
    
    # Find zero gamma level
    zero_crossing = aggregated_df.iloc[(aggregated_df['gamma_exposure'].abs()).argmin()]['strike']
    fig.add_vline(
        x=zero_crossing,
        line_dash="dot",
        line_color="orange",
        annotation_text=f"Zero Gamma: ${zero_crossing:.2f}",
        annotation_position="bottom"
    )
    
    fig.update_layout(
        title=f'{ticker} Gamma Exposure by Strike',
        xaxis_title='Strike Price',
        yaxis_title='Gamma Exposure',
        template='plotly_white',
        hovermode='x unified',
        height=500,
        showlegend=False
    )
    
    return fig


def create_gamma_profile_chart(
    gamma_df: pd.DataFrame,
    current_price: float,
    ticker: str
) -> go.Figure:
    """
    Create gamma profile chart showing calls vs puts
    
    Args:
        gamma_df: DataFrame with gamma exposure by option type
        current_price: Current price of underlying
        ticker: Ticker symbol
        
    Returns:
        Plotly figure
    """
    # Separate calls and puts
    calls_df = gamma_df[gamma_df['type'] == 'call'].groupby('strike')['gamma_exposure'].sum().reset_index()
    puts_df = gamma_df[gamma_df['type'] == 'put'].groupby('strike')['gamma_exposure'].sum().reset_index()
    
    fig = go.Figure()
    
    # Add calls
    if not calls_df.empty:
        fig.add_trace(go.Scatter(
            x=calls_df['strike'],
            y=calls_df['gamma_exposure'],
            mode='lines+markers',
            name='Calls',
            line=dict(color='red', width=2),
            fill='tozeroy',
            fillcolor='rgba(255, 0, 0, 0.1)'
        ))
    
    # Add puts
    if not puts_df.empty:
        fig.add_trace(go.Scatter(
            x=puts_df['strike'],
            y=puts_df['gamma_exposure'],
            mode='lines+markers',
            name='Puts',
            line=dict(color='green', width=2),
            fill='tozeroy',
            fillcolor='rgba(0, 255, 0, 0.1)'
        ))
    
    # Add current price line
    fig.add_vline(
        x=current_price,
        line_dash="dash",
        line_color="blue",
        annotation_text=f"Current: ${current_price:.2f}"
    )
    
    fig.update_layout(
        title=f'{ticker} Gamma Profile: Calls vs Puts',
        xaxis_title='Strike Price',
        yaxis_title='Gamma Exposure',
        template='plotly_white',
        hovermode='x unified',
        height=500,
        legend=dict(x=0.01, y=0.99)
    )
    
    return fig


def create_open_interest_chart(
    options_df: pd.DataFrame,
    current_price: float,
    ticker: str
) -> go.Figure:
    """
    Create open interest distribution chart
    
    Args:
        options_df: DataFrame with options data
        current_price: Current price of underlying
        ticker: Ticker symbol
        
    Returns:
        Plotly figure
    """
    # Aggregate open interest by strike and type
    oi_data = options_df.groupby(['strike', 'type'])['oi'].sum().reset_index()
    
    calls_oi = oi_data[oi_data['type'] == 'call']
    puts_oi = oi_data[oi_data['type'] == 'put']
    
    fig = go.Figure()
    
    # Add calls OI
    if not calls_oi.empty:
        fig.add_trace(go.Bar(
            x=calls_oi['strike'],
            y=calls_oi['oi'],
            name='Calls OI',
            marker_color='lightcoral',
            opacity=0.7
        ))
    
    # Add puts OI
    if not puts_oi.empty:
        fig.add_trace(go.Bar(
            x=puts_oi['strike'],
            y=puts_oi['oi'],
            name='Puts OI',
            marker_color='lightgreen',
            opacity=0.7
        ))
    
    # Add current price line
    fig.add_vline(
        x=current_price,
        line_dash="dash",
        line_color="blue",
        annotation_text=f"Current: ${current_price:.2f}"
    )
    
    fig.update_layout(
        title=f'{ticker} Open Interest Distribution',
        xaxis_title='Strike Price',
        yaxis_title='Open Interest',
        template='plotly_white',
        barmode='group',
        height=400,
        legend=dict(x=0.01, y=0.99)
    )
    
    return fig


def create_metrics_summary(key_levels: dict) -> str:
    """
    Create formatted metrics summary
    
    Args:
        key_levels: Dictionary with key gamma levels
        
    Returns:
        Formatted HTML string
    """
    if not key_levels:
        return "<p>No data available</p>"
    
    html = f"""
    <div style='background-color: #f0f2f6; padding: 20px; border-radius: 10px;'>
        <h3 style='margin-top: 0;'>📊 Key Gamma Levels</h3>
        <table style='width: 100%; border-collapse: collapse;'>
            <tr>
                <td style='padding: 10px;'><strong>Zero Gamma Level:</strong></td>
                <td style='padding: 10px;'>${key_levels['zero_gamma_level']:.2f}</td>
            </tr>
            <tr style='background-color: #e8f4f8;'>
                <td style='padding: 10px;'><strong>Max Positive GEX Strike:</strong></td>
                <td style='padding: 10px;'>${key_levels['max_positive_strike']:.2f}</td>
            </tr>
            <tr>
                <td style='padding: 10px;'><strong>Max Positive GEX Value:</strong></td>
                <td style='padding: 10px;'>{key_levels['max_positive_gex']:,.0f}</td>
            </tr>
            <tr style='background-color: #e8f4f8;'>
                <td style='padding: 10px;'><strong>Max Negative GEX Strike:</strong></td>
                <td style='padding: 10px;'>${key_levels['max_negative_strike']:.2f}</td>
            </tr>
            <tr>
                <td style='padding: 10px;'><strong>Max Negative GEX Value:</strong></td>
                <td style='padding: 10px;'>{key_levels['max_negative_gex']:,.0f}</td>
            </tr>
            <tr style='background-color: #e8f4f8;'>
                <td style='padding: 10px;'><strong>Total Gamma Exposure:</strong></td>
                <td style='padding: 10px;'>{key_levels['total_gamma_exposure']:,.0f}</td>
            </tr>
        </table>
    </div>
    """
    return html
