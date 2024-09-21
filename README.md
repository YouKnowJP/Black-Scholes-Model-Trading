# Black-Scholes-Model-Trading

## Overview

This project implements a comprehensive Black-Scholes trading model for pricing European options and executing delta hedging strategies. The model includes option pricing functions, Greeks calculations, and a basic delta hedging example using Python.

## Features

- **Option Pricing:** Calculate the theoretical price of European call and put options using the Black-Scholes formula.
- **Greeks Calculation:** Compute option sensitivities including Delta, Gamma, Theta, Vega, and Rho.
- **Delta Hedging:** Demonstrate a basic delta hedging strategy.
- **Visualization:** Plot Delta as a function of the underlying asset price.

## Requirements

- Python 3.x
- NumPy
- SciPy
- Pandas
- Matplotlib

## Installation

1. **Clone the Repository:**

    ```bash
    git clone https://github.com/yourusername/black-scholes-trading-model.git
    cd black-scholes-trading-model
    ```

2. **Create a Virtual Environment (Optional but Recommended):**

    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install Dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

    *If `requirements.txt` is not provided, install manually:*

    ```bash
    pip install numpy scipy pandas matplotlib
    ```

## Usage

Run the main script to calculate option prices, Greeks, and perform delta hedging:

```bash
python main.py
