#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep 21 15:32:08 2024

@author: youknowjp
"""

import numpy as np
import scipy.stats as si
from alpha_vantage.timeseries import TimeSeries

# Function to fetch real-time stock price using Alpha Vantage API
def get_stock_price(symbol):
    api_key = 'your_alpha_vantage_api_key'  # Replace with your Alpha Vantage API key
    ts = TimeSeries(key=api_key, output_format='pandas')
    data, meta_data = ts.get_quote_endpoint(symbol)
    return float(data['05. price'][0])

# Function to calculate the Black-Scholes option price
def black_scholes(S, K, T, r, sigma, option_type='call'):
    d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)

    if option_type == 'call':
        return (S * si.norm.cdf(d1, 0.0, 1.0) - K * np.exp(-r * T) * si.norm.cdf(d2, 0.0, 1.0))
    elif option_type == 'put':
        return (K * np.exp(-r * T) * si.norm.cdf(-d2, 0.0, 1.0) - S * si.norm.cdf(-d1, 0.0, 1.0))

# Function to price both call and put options
def price_options(symbol, K, T, r, sigma):
    stock_price = get_stock_price(symbol)
    call_price = black_scholes(stock_price, K, T, r, sigma, option_type='call')
    put_price = black_scholes(stock_price, K, T, r, sigma, option_type='put')
    return call_price, put_price

# Example usage
symbol = 'AAPL'  # Replace with the desired ticker symbol
K = 150  # Strike price
T = 1  # Time to maturity (in years)
r = 0.05  # Risk-free rate (5%)
sigma = 0.25  # Volatility (25%)

call_price, put_price = price_options(symbol, K, T, r, sigma)

print(f"The price of the call option for {symbol} is: {call_price}")
print(f"The price of the put option for {symbol} is: {put_price}")
