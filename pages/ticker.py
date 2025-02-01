import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from services.yahoofinance import YahooFinance

st.markdown(
    r"""
    <style>
    [data-testid="stSidebarCollapsedControl"] {
        display: none;
    }
    [data-testid="stSidebar"] {
        display: none;
    }
    .stAppHeader {
        border-bottom: 1px solid grey;
    }
    .stAppDeployButton {
        visibility: hidden;
        display: none;
    }
    </style>
    """, unsafe_allow_html=True
)
st.title('🎈 Ticker Details')

# Get ticker from query params
ticker = st.query_params["name"]

if ticker:
    print(f"Ticker: {ticker}")
    # Date pickers for selecting timeframe
    today = datetime.today()
    default_start_date = today - timedelta(days=160)
    start_date = st.date_input('Start date', value=default_start_date, max_value=today)
    end_date = st.date_input('End date', value=today, max_value=today)

    # Fetch and display stock data
    yf_service = YahooFinance()
    stock_data = yf_service.get_stock_data(ticker, start=start_date.strftime('%Y-%m-%d'), end=end_date.strftime('%Y-%m-%d'))
    st.write(f"## {ticker} Stock Data")
    st.line_chart(stock_data['Close'])
else:
    st.write("No ticker selected.")
