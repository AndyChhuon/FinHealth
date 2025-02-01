import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from services.yahoofinance import YahooFinance
from yahoo_fin import stock_info as si
import yfinance as yf

st.markdown(
    r"""
    <style>
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
    default_start_date = st.query_params["startDate"] if "startDate" in st.query_params else today - timedelta(days=160)
    default_end_date = st.query_params["endDate"] if "endDate" in st.query_params else today
    start_date = st.date_input('Start date', value=default_start_date, max_value=today)
    end_date = st.date_input('End date', value=default_end_date, max_value=today)

    # Fetch and display stock data
    yf_service = YahooFinance()
    stock_data = yf_service.get_stock_data(ticker, start=start_date.strftime('%Y-%m-%d'), end=end_date.strftime('%Y-%m-%d'))
    st.write(f"## {ticker} Stock Data")
    st.line_chart(stock_data['Close'])

    # Fetch news regarding data and display
    ticker_obj = yf.Ticker(ticker)
    news_data = ticker_obj.get_news()
    st.write(f"## {ticker} News")

    # Display news in a grid with 3 items per row
    for i in range(0, len(news_data), 3):
        cols = st.columns(3)
        for col, news in zip(cols, news_data[i:i+3]):
            content = news['content']
            thumbnail_url = content['thumbnail']['resolutions'][0]['url']
            title = content['title']
            summary = content['summary']
            for key in content.keys():
                print(key)
            print(content)
            link = content['canonicalUrl']['url']
            if len(summary) > 250:
                summary = summary[:250] + "..."

            with col:
                print('sdfds')
                print(content['clickThroughUrl'])
                print(link)
                st.markdown(
                    f"""
                    <a href="{link}" target="_blank" style="text-decoration: none;">
                        <div style="border: 1px solid #e6e6e6; border-radius: 10px; padding: 10px; margin: 10px 0;">
                            <img src="{thumbnail_url}" style="width: 100%; border-radius: 10px;">
                            <h3 style="color: white;">{title}</h3>
                            <p style="color: white;">{summary}</p>
                        </div>
                    </a>
                    """,
                    unsafe_allow_html=True
                )

else:
    st.write("No ticker selected.")
