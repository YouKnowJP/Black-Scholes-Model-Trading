#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep 21 14:58:50 2024

@author: youknowjp
"""

import numpy as np
import matplotlib.pyplot as plt
from black_scholes import black_scholes_price, black_scholes_greeks

def main():
    # Example Parameters
    S = 100        # Current stock price
    K = 100        # Strike price
    T = 1          # Time to maturity (1 year)
    r = 0.05       # Risk-free rate (5%)
    sigma = 0.2    # Volatility (20%)
    option_type = 'call'
    
    # Calculate Option Price
    price = black_scholes_price(S, K, T, r, sigma, option_type)
    print(f"Option Price ({option_type.capitalize()}): {price:.4f}")
    
    # Calculate Greeks
    greeks = black_scholes_greeks(S, K, T, r, sigma, option_type)
    for greek, value in greeks.items():
        print(f"{greek}: {value:.4f}")
    
    # Delta Hedging Example
    # Assume you hold 1 call option
    option_delta = greeks['Delta']
    # To delta hedge, short delta shares
    hedge_shares = -option_delta
    print(f"Number of Shares to Hedge: {hedge_shares:.4f}")
    
    # Visualization of Delta as a function of underlying price
    S_range = np.linspace(50, 150, 100)
    delta_values = [black_scholes_greeks(s, K, T, r, sigma, option_type)['Delta'] for s in S_range]
    
    plt.figure(figsize=(10,6))
    plt.plot(S_range, delta_values, label='Delta', color='blue')
    plt.title('Delta vs. Underlying Asset Price')
    plt.xlabel('Underlying Price ($)')
    plt.ylabel('Delta')
    plt.legend()
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    main()
