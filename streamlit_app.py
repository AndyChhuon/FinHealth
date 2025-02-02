import streamlit as st
import pandas as pd
import json
from datetime import datetime, timedelta

# Additional imports for news and sentiment
import yfinance as yf
from services.sentimentAnalyzer import SentimentAnalyzer

from services.yahoofinance import YahooFinance
from modules.chatbot import chatbot
from modules.stock_graph import stock_graph
from st_pages import add_page_title, get_nav_from_toml

st.set_page_config(layout="wide")

# Sidebar
with st.sidebar:
    st.logo("assets/chart_icon.png")
    st.html("")
    st.page_link(page='http://localhost:8501/', label="Home")
    st.page_link(page='http://localhost:8501/analysis', label="Personal Analysis")

# Custom CSS
st.markdown(
    r"""
    <style>
    .stAppHeader {
        border-bottom: 1px solid grey;
    }
    .stAppToolbar {
        top: 15px;
    }
    .stAppDeployButton {
        visibility: hidden;
        display: none;
    }
    .st-emotion-cache-hzo1qh {
        top: 11px;
    }
    .st-emotion-cache-6qob1r {
        border-right: 1px solid grey;
    }
    .stSidebar {
        width: 220px !important;
        background-color: rgb(25 29 37);
    }
    .st-emotion-cache-kgpedg {
        align-items: center;
        padding: 1rem 1.5rem 1.5rem 1rem;
    }
    .st-emotion-cache-13lvdqn {
        height: 2rem;
    }
    .st-emotion-cache-1p2n2i4 {
        position: relative;
    }
    /* Uncomment if you want hover effect on the cards:
    .stock-cards:hover {
        cursor: pointer;
        background-color: rgb(28, 34, 46) !important;
        transition: 0.2s;
    }
    */
    .stock-details:hover {
        transform: scale(1.05);
        transition: 0.3s;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Define two columns: left (stock_col), right (detail_col)
stock_col, detail_col = st.columns([0.7, 0.3], gap="medium")

# ------------------------------
# LEFT COLUMN: Title, search, date pickers, data fetching
# ------------------------------
with stock_col:
    st.title('Stock Graph')

    # Define top 15 companies
    top_companies = [
        "NVDA",
        "META",
        "TSLA",
        "MSFT",
        "AMZN",
        "AAPL",
        "GOOGL",
        "AMD",
        "NFLX",
        "AVGO"
    ]

    # Initialize search input field
    search_query = st.text_input("Search for a stock", "")

    # Date pickers for selecting timeframe
    today = datetime.today()
    default_start_date = today - timedelta(days=160)
    start_col, end_col = st.columns(2)
    with start_col:
        start_date = st.date_input('Start date', value=default_start_date, max_value=today)
    with end_col:
        end_date = st.date_input('End date', value=today, max_value=today)

    # Add a search bar with stock recommendations
    with open("files/company_tickers_sec.json") as f:
        company_tickers = json.load(f)

    if search_query:
        matching_stocks = [
            company
            for company in company_tickers
            if search_query.lower() in company.lower()
        ]
        if matching_stocks:
            selected_stock = st.selectbox("Select a stock", matching_stocks)
            st.link_button(
                "Go",
                url=f"/ticker?name={company_tickers[selected_stock]}&startDate={start_date}&endDate={end_date}"
            )

    # Example display of a default graph (AAPL)
    stock_graph("AAPL", start_date, end_date)

    # Optional function to display stock data
    def display_stock_data(ticker):
        yf_service = YahooFinance()
        stock_data = yf_service.get_stock_data(
            ticker,
            start=start_date.strftime('%Y-%m-%d'),
            end=end_date.strftime('%Y-%m-%d')
        )
        st.write(f"## {ticker} Stock Data")
        st.line_chart(stock_data['Close'])

    # Fetch data for all top companies once
    yf_service = YahooFinance()
    top_companies_data = {
        company: yf_service.get_stock_data(
            company,
            start=start_date.strftime('%Y-%m-%d'),
            end=end_date.strftime('%Y-%m-%d')
        )
        for company in top_companies
    }
    # Include the chatbot
    chatbot()

# ------------------------------
# RIGHT COLUMN: Display "cards" for top companies, THEN news
# ------------------------------
with detail_col:
    st.header("Top Companies")
    for company in top_companies:
        data = top_companies_data.get(company)
        if data is None or data.empty:
            continue

        last_close = round(data["Close"].iloc[-1], 2)
        first_close = data["Close"].iloc[0]
        pct_change = round((last_close - first_close) / first_close * 100, 2)

        # Card-like div
        st.markdown(
            f"""
            <div class="stock-cards" onclick="location.href='/ticker?name={company}&startDate={start_date}&endDate={end_date}';" style="
                        border: 1px solid #ddd; 
                        border-radius: 5px; 
                        padding: 10px; 
                        background-color: transparent;
                        margin-bottom: 10px;">
                <div style="
                        display: flex;
                        flex-direction: row;
                        justify-content: space-between;
                        width: 100%;
                        align-items: center;">
                    <div style="
                        display: flex;
                        flex-direction: column;
                        align-items: flex-start">
                            <h4 style="margin:0; padding: 0">{company}</h4>
                            <div style="
                                display: flex;
                                flex-direction: row;
                                align-items: flex-start;
                                gap: 10px;">
                            <p style="margin:0;">Price: {last_close}</p>
                            <p style="margin:0; color: {'green' if pct_change >= 0 else 'red'};">
                                {pct_change}%
                            </p>
                            </div>
                    </div>
                    <a class="stock-details" target="_self" href="/ticker?name={company}&startDate={start_date}&endDate={end_date}" style="
                        text-decoration: none; 
                        color: inherit;
                        padding: 3px 7px 3px 7px;
                        border: 1px solid white;
                        border-radius: 10px;
                        height: 40px;
                        align-items: center;
                        display: flex;">View Details</a>
                    </div>
                </div>
            """,
            unsafe_allow_html=True
        )

    # ----------------------------------
    # NEWS SECTION (similar to ticker.py)
    # ----------------------------------
    st.header("Latest News")

    # For demonstration, we pick a default ticker
    default_ticker = "AAPL"
    ticker_obj = yf.Ticker(default_ticker)
    news_data = ticker_obj.get_news()

    # Custom CSS for the news display
    # Custom CSS for the news display
    st.markdown(
        """
        <style>
        .news-box {
            border: 1px solid #e6e6e6;
            border-radius: 10px;
            padding: 10px;
            margin-bottom: 15px; 
            overflow: hidden;
            display: flex;
            flex-direction: row;
            background-color: #1e1e1e;
            gap: 10px;
        }
        .news-desc {
            display: flex;
            flex-direction: column;
            gap: 10px;
        }
        .news-box img {
            border-radius: 10px;
            width: 150px;
            object-fit: cover;
        }
        .news-box h3 {
            color: white;
            font-size: 1.1em;
            margin: 0;
            line-height: 1.2; 
            padding: 0;
        }
        .news-box p {
            color: white;
            font-size: 0.9em; 
            margin: 0; 
            overflow: hidden;
            text-overflow: ellipsis;
            display: -webkit-box;
            -webkit-line-clamp: 3;
            -webkit-box-orient: vertical;
        }
        .stMarkdownContainer {
            padding: 0;
        }
        /* Remove or adjust this if you prefer a different layout. */
        .stHorizontalContainer {
            display: flex;
            flex-wrap: wrap; 
            justify-content: space-between; 
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Display each news item in a single column from top to bottom
    for news in news_data:
        content = news['content']

        # Safely extract thumbnail URL
        thumbnail_url = None
        if content.get('thumbnail') and content['thumbnail'].get('resolutions'):
            thumbnail_url = content['thumbnail']['resolutions'][0]['url']

        title = content.get('title', "No Title")
        summary = content.get('summary', "No Summary")
        link = content.get('canonicalUrl', {}).get('url', "#")

        st.markdown(
            f"""
            <a href="{link}" target="_blank" style="text-decoration: none;">
                <div class="news-box">
                    <img src="{thumbnail_url or ''}">
                    <div class="news-desc"> 
                    <h3>{title}</h3>
                    <p>{summary}</p>
                    </div>
                </div>
            </a>
            """,
            unsafe_allow_html=True
        )

