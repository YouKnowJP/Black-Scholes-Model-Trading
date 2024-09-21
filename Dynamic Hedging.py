#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep 21 15:02:18 2024

@author: youknowjp
"""

import numpy as np
import pandas as pd
from black_scholes import black_scholes_price, black_scholes_greeks
import matplotlib.pyplot as plt
import logging

def simulate_dynamic_hedging(S0, K, T, r, sigma, option_type='call', 
                             steps=252, transaction_cost=0.001):
    """
    Simulate dynamic delta hedging over the option's life.

    Parameters:
    S0 : float
        Initial stock price
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
    steps : int
        Number of time steps
    transaction_cost : float
        Transaction cost per trade (as a fraction)

    Returns:
    dict
        Portfolio performance metrics
    """
    dt = T / steps
    times = np.linspace(0, T, steps + 1)
    # Simulate underlying asset price using Geometric Brownian Motion
    np.random.seed(42)  # For reproducibility
    price_paths = [S0]
    for _ in range(steps):
        Z = np.random.standard_normal()
        S_prev = price_paths[-1]
        S_new = S_prev * np.exp((r - 0.5 * sigma**2)*dt + sigma * np.sqrt(dt) * Z)
        price_paths.append(S_new)
    
    price_paths = np.array(price_paths)
    portfolio_values = []
    hedge_positions = []
    cash_positions = []
    transaction_costs = []
    
    # Initial option price and Delta
    option_price = black_scholes_price(S0, K, T, r, sigma, option_type)
    greeks = black_scholes_greeks(S0, K, T, r, sigma, option_type)
    delta = greeks['Delta']
    
    # Initial hedge: short delta shares
    hedge = -delta
    cash = option_price + hedge * S0 - abs(hedge) * S0 * transaction_cost
    total_portfolio = cash + hedge * S0
    portfolio_values.append(total_portfolio)
    hedge_positions.append(hedge)
    cash_positions.append(cash)
    transaction_costs.append(abs(hedge) * S0 * transaction_cost)
    
    for i in range(1, len(times)):
        t = times[i]
        S = price_paths[i]
        tau = T - t
        if tau <= 0:
            tau = 1e-6  # Avoid division by zero
        
        # Recalculate option price and Delta
        option_price = black_scholes_price(S, K, tau, r, sigma, option_type)
        greeks = black_scholes_greeks(S, K, tau, r, sigma, option_type)
        new_delta = greeks['Delta']
        
        # Adjust hedge
        new_hedge = -new_delta
        delta_change = new_hedge - hedge
        cost = abs(delta_change) * S * transaction_cost
        transaction_costs.append(cost)
        
        # Update cash position
        cash = cash * np.exp(r * dt) + hedge * (price_paths[i] - price_paths[i-1]) - cost
        
        # Update hedge
        hedge = new_hedge
        hedge_positions.append(hedge)
        cash_positions.append(cash)
        
        # Total portfolio value
        total_portfolio = cash + hedge * S
        portfolio_values.append(total_portfolio)
    
    # At maturity, settle the option
    final_option_payoff = max(price_paths[-1] - K, 0) if option_type.lower() == 'call' else max(K - price_paths[-1], 0)
    final_portfolio = portfolio_values[-1] + final_option_payoff
    portfolio_values[-1] = final_portfolio
    
    # Metrics
    total_return = (final_portfolio - option_price) / option_price
    max_drawdown = calculate_max_drawdown(portfolio_values)
    
    # Logging
    logging.info(f"Dynamic Hedging Simulation Completed")
    logging.info(f"Total Return: {total_return*100:.2f}%")
    logging.info(f"Maximum Drawdown: {max_drawdown*100:.2f}%")
    
    # Visualization
    plt.figure(figsize=(12,6))
    plt.plot(times, portfolio_values, label='Portfolio Value')
    plt.title('Dynamic Delta Hedging Portfolio Value Over Time')
    plt.xlabel('Time (Years)')
    plt.ylabel('Portfolio Value ($)')
    plt.legend()
    plt.grid(True)
    plt.show()
    
    return {
        'Total Return': total_return,
        'Maximum Drawdown': max_drawdown,
        'Final Portfolio Value': final_portfolio,
        'Portfolio Values': portfolio_values,
        'Hedge Positions': hedge_positions,
        'Cash Positions': cash_positions,
        'Transaction Costs': transaction_costs,
        'Price Paths': price_paths
    }

def calculate_max_drawdown(portfolio_values):
    """
    Calculate the maximum drawdown of the portfolio.

    Parameters:
    portfolio_values : list or array
        Portfolio values over time

    Returns:
    float
        Maximum drawdown as a fraction
    """
    peak = portfolio_values[0]
    max_dd = 0
    for value in portfolio_values:
        if value > peak:
            peak = value
        drawdown = (peak - value) / peak
        if drawdown > max_dd:
            max_dd = drawdown
    return max_dd
