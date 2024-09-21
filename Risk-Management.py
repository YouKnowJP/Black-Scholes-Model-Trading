#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep 21 15:03:12 2024

@author: youknowjp
"""

import logging

def calculate_position_size(account_size, risk_per_trade, stop_loss_distance, current_price):
    """
    Calculate the number of shares to trade based on risk management rules.

    Parameters:
    account_size : float
        Total size of the trading account
    risk_per_trade : float
        Fraction of account to risk per trade (e.g., 0.01 for 1%)
    stop_loss_distance : float
        Distance to stop loss from entry price (in dollars)
    current_price : float
        Current price of the asset

    Returns:
    int
        Number of shares to trade
    """
    risk_amount = account_size * risk_per_trade
    position_size = risk_amount / stop_loss_distance
    position_size = int(position_size)  # Round down to nearest whole share
    logging.info(f"Calculated Position Size: {position_size} shares")
    return position_size

def implement_stop_loss(current_position, entry_price, current_price, stop_loss_threshold):
    """
    Determine whether to trigger a stop-loss.

    Parameters:
    current_position : int
        Current number of shares held (positive for long, negative for short)
    entry_price : float
        Price at which the position was entered
    current_price : float
        Current price of the asset
    stop_loss_threshold : float
        Threshold for stop loss (e.g., 0.95 for 5% loss)

    Returns:
    bool
        True if stop-loss is triggered, False otherwise
    """
    if current_position > 0:
        # Long position
        if current_price <= entry_price * stop_loss_threshold:
            logging.warning(f"Stop-loss triggered for long position at {current_price}")
            return True
    elif current_position < 0:
        # Short position
        if current_price >= entry_price / stop_loss_threshold:
            logging.warning(f"Stop-loss triggered for short position at {current_price}")
            return True
    return False
