import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta
import pytz
import ta
from datetime import date

def get_stock_data(symbol: str, start: str, end: str, interval) -> pd.DataFrame:
    stock = yf.Ticker(symbol)
    df = stock.history(start=start, end=end, interval=interval)
    return df

def process_data(data):
    if data.index.tzinfo is None:
        data.index = data.index.tz_localize('UTC')
    data.index = data.index.tz_convert('US/Eastern')
    data.reset_index(inplace=True)
    data.rename(columns={'Date': 'Datetime'}, inplace=True)
    return data

def calculate_metrics(data):
    last_close = data['Close'].iloc[-1]
    prev_close = data['Close'].iloc[0]
    change = last_close - prev_close
    pct_change = (change / prev_close) * 100
    high = data['High'].max()
    low = data['Low'].min()
    volume = data['Volume'].sum()
    return last_close, change, pct_change, high, low, volume


# Add simple moving average (SMA) and exponential moving average (EMA) indicators
def add_technical_indicators(data):
    data['SMA_20'] = ta.trend.sma_indicator(data['Close'], window=20)
    data['EMA_20'] = ta.trend.ema_indicator(data['Close'], window=20)
    return data

def get_interval(start_date: date, end_date: date) -> str:
    
    period = (end_date - start_date).days
    print(period)
    
    if period <= 1:
        return '15m'
    elif period <= 7:
        return '30m'
    elif period <= 32:
        return '1d'
    else:
        return '1wk'

def stock_graph(symbol: str, start: date, end: date):
    st.title("Stock Graph")

    interval = get_interval(start_date=start, end_date=end)
    print(interval)
    data = get_stock_data(symbol=symbol, start=start, end=end, interval=interval)
    data = process_data(data)
    data = add_technical_indicators(data)
    last_close, change, pct_change, high, low, volume = calculate_metrics(data)

    st.metric(label=f"{symbol} Last Price", value=f"{last_close:.2f} USD", delta=f"{change:.2f} ({pct_change:.2f}%)")

    col1, col2, col3 = st.columns(3)
    col1.metric("High", f"{high:.2f} USD")
    col2.metric("Low", f"{low:.2f} USD")
    col3.metric("Volume", f"{volume:,}")
    
    # Plot the stock price chart
    fig = go.Figure()

    fig.add_trace(go.Candlestick(x=data['Datetime'],
                                open=data['Open'],
                                high=data['High'],
                                low=data['Low'],
                                close=data['Close']))
    
    fig.add_trace(go.Scatter(x=data['Datetime'], 
                                y=data['Close'], 
                                mode='lines', 
                                name="Closing Price",
                                line=dict(color='blue', width=2)))

    # fig = px.line(data, x='Datetime', y='Close')
    

    # fig.add_trace(go.Scatter(x=data['Datetime'], y=data['SMA_20'], name='SMA 20'))
    # fig.add_trace(go.Scatter(x=data['Datetime'], y=data['EMA_20'], name='EMA 20'))
    
    # Format graph
    fig.update_layout(title=f'{symbol} Chart',
                      xaxis_title='Time',
                      yaxis_title='Price (USD)',
                      height=600)
    st.plotly_chart(fig, use_container_width=True)
    print(end, start)


if __name__ == "__main__":
    data = get_stock_data("AAPL", "2024-01-01", "2024-02-01")
    print(data)