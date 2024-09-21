#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep 21 14:58:50 2024

@author: youknowjp
"""

import numpy as np
import matplotlib.pyplot as plt
from black_scholes import black_scholes_price, black_scholes_greeks
from dynamic_hedging import simulate_dynamic_hedging
import logging

# Configure Logging
logging.basicConfig(filename='logs/trading.log', 
                    level=logging.INFO,
                    format='%(asctime)s %(levelname)s:%(message)s')

def main():
    # Example Parameters
    S0 = 100        # Initial stock price
    K = 100         # Strike price
    T = 1           # Time to maturity (1 year)
    r = 0.05        # Risk-free rate (5%)
    sigma = 0.2     # Volatility (20%)
    option_type = 'call'
    steps = 252     # Daily steps
    transaction_cost = 0.001  # 0.1% per trade

    logging.info("Starting Dynamic Hedging Simulation")
    
    # Run Dynamic Hedging Simulation
    results = simulate_dynamic_hedging(S0, K, T, r, sigma, option_type, steps, transaction_cost)
    
    # Output Results
    print(f"Dynamic Hedging Simulation Completed")
    print(f"Total Return: {results['Total Return']*100:.2f}%")
    print(f"Maximum Drawdown: {results['Maximum Drawdown']*100:.2f}%")
    print(f"Final Portfolio Value: ${results['Final Portfolio Value']:.2f}")
    
    # Additional analysis can be added here

if __name__ == "__main__":
    main()
