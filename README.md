# M7 Dashboard

Welcome to the M7 Dashboard, a Streamlit application designed to visualize stock data for the Magnificent 7 stocks. This dashboard allows users to select a stock, view its historical data, and analyze various metrics through interactive charts.

## Features

- **Stock Selection**: Choose from the Magnificent 7 stocks: Apple (AAPL), Microsoft (MSFT), Google (GOOGL), Amazon (AMZN), Nvidia (NVDA), Tesla (TSLA), and Meta (META).
- **Historical Data**: Displays the last 3 days of stock data.
- **Key Metrics**: Shows the latest close date, close price, trading volume, and daily volatility.
- **Charts**:
  - **Candlestick Chart**: With 10-day and 20-day moving averages.
  - **Volume Chart**: Daily trading volume.

## Requirements

Ensure you have the following Python packages installed:

- `streamlit`
- `yfinance`
- `pandas`
- `plotly`

You can install the required packages using pip:

```bash
pip install -r requirements.txt
