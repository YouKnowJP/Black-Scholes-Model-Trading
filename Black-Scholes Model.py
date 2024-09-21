#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep 21 14:58:03 2024

@author: youknowjp
"""

### black_scholes.py

import numpy as np
from scipy.stats import norm

def black_scholes_price(S, K, T, r, sigma, option_type='call'):
    """
    Calculate Black-Scholes option price for European call or put.

    Parameters:
    S : float
        Current stock price
    K : float
        Strike price
    T : float
        Time to maturity (in years)
    r : float
        Risk-free interest rate
    sigma : float
        Volatility of the underlying asset
    option_type : str
        'call' or 'put'

    Returns:
    float
        Option price
    """
    if T <= 0:
        # Option has expired
        if option_type.lower() == 'call':
            return max(S - K, 0.0)
        elif option_type.lower() == 'put':
            return max(K - S, 0.0)
        else:
            raise ValueError("option_type must be 'call' or 'put'")
    
    d1 = (np.log(S / K) + (r + 0.5 * sigma **2 ) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    
    if option_type.lower() == 'call':
        price = S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
    elif option_type.lower() == 'put':
        price = K * np.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)
    else:
        raise ValueError("option_type must be 'call' or 'put'")
    
    return price

def black_scholes_greeks(S, K, T, r, sigma, option_type='call'):
    """
    Calculate Black-Scholes Greeks for European call or put.

    Parameters:
    S, K, T, r, sigma : same as above
    option_type : 'call' or 'put'

    Returns:
    dict
        Dictionary containing Delta, Gamma, Theta, Vega, Rho
    """
    if T <= 0:
        # Option has expired; Greeks are not defined
        return {
            'Delta': 0.0,
            'Gamma': 0.0,
            'Theta': 0.0,
            'Vega': 0.0,
            'Rho': 0.0
        }
    
    d1 = (np.log(S / K) + (r + 0.5 * sigma **2 ) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    
    if option_type.lower() == 'call':
        delta = norm.cdf(d1)
        theta = (- (S * norm.pdf(d1) * sigma) / (2 * np.sqrt(T)) 
                 - r * K * np.exp(-r * T) * norm.cdf(d2))
        rho = K * T * np.exp(-r * T) * norm.cdf(d2)
    elif option_type.lower() == 'put':
        delta = norm.cdf(d1) - 1
        theta = (- (S * norm.pdf(d1) * sigma) / (2 * np.sqrt(T)) 
                 + r * K * np.exp(-r * T) * norm.cdf(-d2))
        rho = -K * T * np.exp(-r * T) * norm.cdf(-d2)
    else:
        raise ValueError("option_type must be 'call' or 'put'")
    
    gamma = norm.pdf(d1) / (S * sigma * np.sqrt(T))
    vega = S * norm.pdf(d1) * np.sqrt(T)
    
    return {
        'Delta': delta,
        'Gamma': gamma,
        'Theta': theta,
        'Vega': vega,
        'Rho': rho
    }
