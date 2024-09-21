#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep 21 15:03:48 2024

@author: youknowjp
"""

import pandas as pd
from black_scholes import black_scholes_price, black_scholes_greeks
from risk_management import calculate_position_size, implement_stop_loss
import logging

def run_backtest(data, K, T, r, sigma, option_type='call', 
                transaction_cost=0.001, risk_per_trade=0.01, 
                stop_loss_threshold=0.95):
    """
    Run backtest on historical data.

    Parameters:
    data : DataFrame
        Historical price data with 'Close' prices
    K : float
        Strike price
    T : float
        Time to maturity (in years)
    r : float
        Risk-free rate
    sigma : float
        Volatility
    option_type : str
        'call' or 'put'
    transaction_cost : float
        Transaction cost per trade
    risk_per_trade : float
        Fraction of account to risk per trade
    stop_loss_threshold : float
        Threshold for stop loss

    Returns:
    dict
        Backtest performance metrics
    """
    account_size = 100000  # Starting with $100,000
    portfolio = account_size
    position = 0
    entry_price = 0
    max_portfolio = portfolio
    drawdown = 0
    max_drawdown = 0
    returns = []
    
    for index, row in data.iterrows():
        S = row['Close']
        if position == 0:
            # Open a new position
            option_price = black_scholes_price(S, K, T, r, sigma, option_type)
            greeks = black_scholes_greeks(S, K, T, r, sigma, option_type)
            delta = greeks['Delta']
            # Calculate position size
            risk_amount = portfolio * risk_per_trade
            position_size = int(risk_amount / 5)  # Assuming stop loss distance of $5
            position = position_size
            entry_price = S
            # Deduct transaction cost
            cost = position_size * S * transaction_cost
            portfolio -= position_size * S + cost
            logging.info(f"Opened position: {position_size} shares at {S}")
        else:
            # Check for stop-loss
            if implement_stop_loss(position, entry_price, S, stop_loss_threshold):
                # Close position
                portfolio += position * S
                # Deduct transaction cost
                cost = position * S * transaction_cost
                portfolio -= cost
                logging.info(f"Closed position: {position} shares at {S}")
                position = 0
                entry_price = 0
        
        # Update portfolio value
        if position > 0:
            portfolio_value = portfolio + position * S
        else:
            portfolio_value = portfolio
        returns.append(portfolio_value)
        
        # Update drawdown
        if portfolio_value > max_portfolio:
            max_portfolio = portfolio_value
        drawdown = (max_portfolio - portfolio_value) / max_portfolio
        if drawdown > max_drawdown:
            max_drawdown = drawdown
    
    total_return = (portfolio_value - account_size) / account_size
    sharpe_ratio = (np.mean(returns) - account_size) / np.std(returns) * np.sqrt(252)
    
    # Logging
    logging.info(f"Backtest Completed")
    logging.info(f"Total Return: {total_return*100:.2f}%")
    logging.info(f"Maximum Drawdown: {max_drawdown*100:.2f}%")
    logging.info(f"Sharpe Ratio: {sharpe_ratio:.2f}")
    
    # Visualization
    data['Portfolio Value'] = returns
    data['Portfolio Value'].plot(figsize=(12,6))
    plt.title('Backtest Portfolio Value Over Time')
    plt.xlabel('Date')
    plt.ylabel('Portfolio Value ($)')
    plt.grid(True)
    plt.show()
    
    return {
        'Total Return': total_return,
        'Maximum Drawdown': max_drawdown,
        'Sharpe Ratio': sharpe_ratio,
        'Final Portfolio Value': portfolio_value,
        'Portfolio Values': returns
    }
