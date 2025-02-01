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
st.title('🎈 Budget Buddy')
# Define top 15 companies
top_companies = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'META', 'TSLA', 'BRK-B', 'JNJ', 'V', 'WMT', 'JPM', 'PG', 'NVDA', 'DIS', 'MA']

# Date pickers for selecting timeframe
today = datetime.today()
default_start_date = today - timedelta(days=160)
start_date = st.date_input('Start date', value=default_start_date, max_value=today)
end_date = st.date_input('End date', value=today, max_value=today)

# Function to display stock data
def display_stock_data(ticker):
    yf_service = YahooFinance()
    stock_data = yf_service.get_stock_data(ticker, start=start_date.strftime('%Y-%m-%d'), end=end_date.strftime('%Y-%m-%d'))
    st.write(f"## {ticker} Stock Data")
    st.line_chart(stock_data['Close'])

# Display top 15 companies
st.write("## Top 15 Companies")
cols = st.columns(3)
for i, company in enumerate(top_companies):
    with cols[i % 3]:
        yf_service = YahooFinance()
        company_data = yf_service.get_stock_data(company, start=start_date.strftime('%Y-%m-%d'), end=end_date.strftime('%Y-%m-%d'))
        st.write(f"### {company}")
        st.line_chart(company_data['Close'])
        st.link_button(f"View {company} details", url=f"/ticker?name={company}")
            
