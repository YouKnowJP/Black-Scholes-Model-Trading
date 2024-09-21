#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep 21 15:03:31 2024

@author: youknowjp
"""

import yfinance as yf
import pandas as pd
import logging
import time

def fetch_live_price(ticker):
    """
    Fetch the latest stock price for the given ticker.

    Parameters:
    ticker : str
        Stock ticker symbol

    Returns:
    float
        Latest stock price
    """
    try:
        stock = yf.Ticker(ticker)
        data = stock.history(period='1m')
        if not data.empty:
            latest_price = data['Close'].iloc[-1]
            logging.info(f"Fetched live price for {ticker}: {latest_price}")
            return latest_price
        else:
            logging.warning(f"No data fetched for {ticker}")
            return None
    except Exception as e:
        logging.error(f"Error fetching live price for {ticker}: {e}")
        return None

def save_live_data(ticker, interval='1m', duration=60):
    """
    Continuously fetch live data for a given duration.

    Parameters:
    ticker : str
        Stock ticker symbol
    interval : str
        Data interval (e.g., '1m' for 1 minute)
    duration : int
        Duration to fetch data in seconds
    """
    end_time = time.time() + duration
    while time.time() < end_time:
        price = fetch_live_price(ticker)
        if price:
            # Append to a CSV file
            df = pd.DataFrame({'Price': [price], 'Timestamp': [pd.Timestamp.now()]})
            df.to_csv(f'data/{ticker}_live.csv', mode='a', header=False, index=False)
        time.sleep(60)  # Wait for 1 minute before next fetch
