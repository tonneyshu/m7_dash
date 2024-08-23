import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta

# Page configuration
st.set_page_config(
    page_title="M7 Dashboard",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Default date range for last 90 days
today = datetime.today()
start_date = today - timedelta(days=90)

# Sidebar
with st.sidebar:
    st.title('📈 M7 Dashboard')
    
    # Dropdown list with "Magnificent 7" stocks
    m7 = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'NVDA', 'TSLA', 'META']
    selected_stock = st.selectbox('Select stock symbol', m7)
    
    start_date = st.date_input('Start date', value=start_date.date())
    end_date = st.date_input('End date', value=today.date())
    st.markdown('### Display Options')
    show_candlestick = st.checkbox('Show Candlestick Chart', value=True)
    show_volume = st.checkbox('Show Volume Chart', value=True)

# Load data
@st.cache_data
def load_stock_data(symbol, start, end):
    data = yf.download(symbol, start=start, end=end)
    data.reset_index(inplace=True)
    return data

# Fetch stock data based on user selection
df = load_stock_data(selected_stock, start_date, end_date)

# Filter to last 3 days for historical data section
df_last_3_days = df.tail(3).sort_values(by='Date', ascending=False)

# Calculate daily volatility (high - low) as percentage of closing price
def calculate_daily_volatility_percentage(df):
    df['Daily Volatility'] = (df['High'] - df['Low']) / df['Close'] * 100
    latest_daily_volatility_percentage = df['Daily Volatility'].iloc[-1] if not df.empty else None
    return latest_daily_volatility_percentage

latest_daily_volatility_percentage = calculate_daily_volatility_percentage(df)

# Calculate moving averages
def calculate_moving_averages(df):
    df['Moving Average 10'] = df['Close'].rolling(window=10).mean()
    df['Moving Average 20'] = df['Close'].rolling(window=20).mean()
    ma10 = df['Moving Average 10'].iloc[-1] if not df.empty else None
    ma20 = df['Moving Average 20'].iloc[-1] if not df.empty else None
    return ma10, ma20

ma10, ma20 = calculate_moving_averages(df)

# Candlestick chart with moving averages
def make_candlestick_chart_with_ma(df):
    fig = go.Figure(data=[go.Candlestick(x=df['Date'],
                                         open=df['Open'],
                                         high=df['High'],
                                         low=df['Low'],
                                         close=df['Close'],
                                         name='Candlestick'),
                          go.Scatter(x=df['Date'], y=df['Moving Average 10'], mode='lines', name='10-Day MA', line=dict(color='orange')),
                          go.Scatter(x=df['Date'], y=df['Moving Average 20'], mode='lines', name='20-Day MA', line=dict(color='red'))])
    fig.update_layout(title='Candlestick Chart with Moving Averages', 
                      xaxis_title='Date', 
                      yaxis_title='Price', 
                      template='plotly_dark', 
                      xaxis_rangeslider_visible=False,
                      height=400, # Adjust height
                      width=800) # Adjust width
    return fig

# Volume chart
def make_volume_chart(df):
    fig = go.Figure(data=[go.Bar(x=df['Date'], y=df['Volume'], name='Volume')])
    fig.update_layout(title='Daily Trading Volume', 
                      xaxis_title='Date', 
                      yaxis_title='Volume', 
                      template='plotly_dark',
                      height=400, # Adjust height
                      width=800) # Adjust width
    return fig

# Key metrics
def display_key_metrics():
    last_close_date = df['Date'].iloc[-1].strftime('%Y-%m-%d') if not df.empty else "N/A"
    last_close_price = f"${df['Close'].iloc[-1]:.2f}" if not df.empty else "N/A"
    last_volume = f"{df['Volume'].iloc[-1]:,.0f}" if not df.empty else "N/A"
    last_volatility = f"{latest_daily_volatility_percentage:.2f}%" if latest_daily_volatility_percentage is not None else "N/A"
    
    st.markdown('### Key Metrics')
    st.metric(label="Last Close Date", value=last_close_date)
    st.metric(label="Last Close Price", value=last_close_price)
    st.metric(label="Last Volume", value=last_volume)
    st.metric(label="Daily Volatility (High-Low %)", value=last_volatility)

# Dashboard Main Panel
col = st.columns((2, 2), gap='small')

with col[0]:
    display_key_metrics()

with col[1]:
    if show_candlestick:
        candlestick_chart = make_candlestick_chart_with_ma(df)
        st.plotly_chart(candlestick_chart, use_container_width=True)

    if show_volume:
        volume_chart = make_volume_chart(df)
        st.plotly_chart(volume_chart, use_container_width=True)

with col[0]:
    st.markdown('### Historical Data (Last 3 Days)')
    st.dataframe(df_last_3_days[['Date', 'Open', 'High', 'Low', 'Close', 'Volume']],
                 column_order=("Date", "Open", "High", "Low", "Close", "Volume"),
                 hide_index=True)
    
    with st.expander('About', expanded=True):
        st.write('''
            - Data Source: [Yahoo Finance](https://finance.yahoo.com).
            - :orange[**Key Metrics**]: Last close date, price, volume, and daily volatility (percentage).
            ''')
