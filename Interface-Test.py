#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep 21 15:04:12 2024

@author: youknowjp
"""

import streamlit as st
import pandas as pd
from backtesting import run_backtest
from dynamic_hedging import simulate_dynamic_hedging
from black_scholes import black_scholes_price, black_scholes_greeks
import yfinance as yf
import matplotlib.pyplot as plt

def main():
    st.title("Black-Scholes Trading Model")
    
    menu = ["Backtest", "Dynamic Hedging", "About"]
    choice = st.sidebar.selectbox("Menu", menu)
    
    if choice == "Backtest":
        st.header("Backtest Trading Strategy")
        ticker = st.text_input("Ticker Symbol", "AAPL")
        start_date = st.date_input("Start Date", pd.to_datetime("2020-01-01"))
        end_date = st.date_input("End Date", pd.to_datetime("2023-12-31"))
        if st.button("Download Data"):
            data = yf.download(ticker, start=start_date, end=end_date)
            data.to_csv(f'data/{ticker}_historical.csv')
            st.write("Data Downloaded Successfully!")
            st.dataframe(data.tail())
        
        if st.button("Run Backtest"):
            data = pd.read_csv(f'data/{ticker}_historical.csv', parse_dates=['Date'], index_col='Date')
            K = st.number_input("Strike Price", value=150.0)
            T = st.number_input("Time to Maturity (Years)", value=0.5)
            r = st.number_input("Risk-Free Rate (%)", value=3.0) / 100
            sigma = st.number_input("Volatility (%)", value=25.0) / 100
            option_type = st.selectbox("Option Type", ["call", "put"])
            transaction_cost = st.number_input("Transaction Cost (%)", value=0.1) / 100
            risk_per_trade = st.number_input("Risk per Trade (%)", value=1.0) / 100
            stop_loss_threshold = st.number_input("Stop-Loss Threshold (%)", value=95.0) / 100
            
            results = run_backtest(data, K, T, r, sigma, option_type, 
                                   transaction_cost, risk_per_trade, stop_loss_threshold)
            
            st.subheader("Backtest Results")
            st.write(f"**Total Return:** {results['Total Return']*100:.2f}%")
            st.write(f"**Maximum Drawdown:** {results['Maximum Drawdown']*100:.2f}%")
            st.write(f"**Sharpe Ratio:** {results['Sharpe Ratio']:.2f}")
            st.write(f"**Final Portfolio Value:** ${results['Final Portfolio Value']:.2f}")
            
            # Display Portfolio Plot
            fig, ax = plt.subplots()
            ax.plot(data.index, results['Portfolio Values'])
            ax.set_title("Portfolio Value Over Time")
            ax.set_xlabel("Date")
            ax.set_ylabel("Portfolio Value ($)")
            st.pyplot(fig)
    
    elif choice == "Dynamic Hedging":
        st.header("Dynamic Delta Hedging Simulation")
        S0 = st.number_input("Initial Stock Price", value=150.0)
        K = st.number_input("Strike Price", value=155.0)
        T = st.number_input("Time to Maturity (Years)", value=0.5)
        r = st.number_input("Risk-Free Rate (%)", value=3.0) / 100
        sigma = st.number_input("Volatility (%)", value=25.0) / 100
        option_type = st.selectbox("Option Type", ["call", "put"])
        steps = st.number_input("Number of Steps", value=252)
        transaction_cost = st.number_input("Transaction Cost (%)", value=0.1) / 100
        account_size = st.number_input("Account Size ($)", value=100000.0)
        risk_per_trade = st.number_input("Risk per Trade (%)", value=1.0) / 100
        stop_loss_distance = st.number_input("Stop-Loss Distance ($)", value=5.0)
        
        if st.button("Run Simulation"):
            results = simulate_dynamic_hedging(S0, K, T, r, sigma, option_type, 
                                              steps, transaction_cost)
            
            st.subheader("Simulation Results")
            st.write(f"**Total Return:** {results['Total Return']*100:.2f}%")
            st.write(f"**Maximum Drawdown:** {results['Maximum Drawdown']*100:.2f}%")
            st.write(f"**Final Portfolio Value:** ${results['Final Portfolio Value']:.2f}")
            
            # Display Portfolio Plot
            fig, ax = plt.subplots()
            ax.plot(np.linspace(0, T, steps+1), results['Portfolio Values'])
            ax.set_title("Portfolio Value Over Time")
            ax.set_xlabel("Time (Years)")
            ax.set_ylabel("Portfolio Value ($)")
            st.pyplot(fig)
    
    elif choice == "About":
        st.header("About")
        st.write("""
        This project implements a comprehensive Black-Scholes trading model for pricing European options and executing delta hedging strategies. 
        It includes option pricing functions, Greeks calculations, dynamic hedging simulation, risk management, backtesting framework, and real-time data integration.
        """)
        st.write("**Disclaimer:** This tool is for educational purposes only and does not constitute financial advice.")

if __name__ == "__main__":
    main()
