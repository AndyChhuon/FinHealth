import streamlit as st
import pandas as pd
import json
from datetime import datetime, timedelta
import yfinance as yf
from services.sentimentAnalyzer import SentimentAnalyzer
from services.yahoofinance import YahooFinance
from modules.stock_graph import get_stock_data, stock_graph
from modules.chatbot import chatbot

st.set_page_config(layout="wide")

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
    /*
    .st-emotion-cache-1p2n2i4 {
        position: relative;
    }
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
    .sidebar-url {
        text-decoration: none;
        color: white; 
        width: 100%;
        border-radius: 7px;
        text-indent: 10px;
        line-height: 32px;
    }
    .sidebar-url:hover {
        background-color: rgb(47, 51, 61);
        cursor: pointer;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ----------------------------------------
# SIDEBAR
# ----------------------------------------
with st.sidebar:
    st.logo("assets/chart_icon.png")
    st.markdown(
            f"""
            <div style="
                display: flex;
                flex-direction: column;
                font-size: 17px;
                gap: 5px;">
            <a class="sidebar-url" href="http://localhost:8501/" target="_self" style="text-decoration: none; color: white; width: 100%">
                Home
            </a>
            <a class="sidebar-url" href="http://localhost:8501/analysis" target="_self" style="text-decoration: none; color: white; width: 100%;">
                Analysis
            </a>
            </div>
            """,
            unsafe_allow_html=True
        )
    #st.page_link(page='http://localhost:8501/', label="Home")
    #st.page_link(page='http://localhost:8501/analysis', label="Personal Analysis")


# ----------------------------------------
# SESSION STATE
# ----------------------------------------
if "messages" not in st.session_state:
    st.session_state["messages"] = []

if "ticker" not in st.session_state:
    st.session_state["ticker"] = "AMZN"

# CAPTURE USER INPUT
user_input = st.chat_input("Ask your question here...")
if user_input:
    # Append user message
    st.session_state["messages"].append({"role": "user", "content": user_input})

stock_col, detail_col = st.columns([0.7, 0.3], gap="medium")

# ----------------------------------------
# LEFT COLUMN
# ----------------------------------------
with stock_col:
    st.title("Stock Graph")

    # Top 10 companies
    top_companies = [
        "NVDA", "META", "TSLA", "MSFT", "AMZN",
        "AAPL", "GOOGL", "AMD", "NFLX", "AVGO"
    ]

    # Basic search + date pickers
    search_query = st.text_input("Search for a stock", "")
    today = datetime.today()
    default_start_date = today - timedelta(days=160)
    start_col, end_col = st.columns(2)
    with start_col:
        start_date = st.date_input("Start date", value=default_start_date, max_value=today)
    with end_col:
        end_date = st.date_input("End date", value=today, max_value=today)

    # Read company tickers from file
    with open("files/company_tickers_sec.json") as f:
        company_tickers = json.load(f)

    if search_query:
        matching_stocks = [
            c for c in company_tickers
            if search_query.lower() in c.lower()
        ]
        if matching_stocks:
            selected_stock = st.selectbox("Select a stock", matching_stocks)
            if st.button("Go"):
                st.session_state["ticker"] = company_tickers[selected_stock]

    # Show selected ticker graph
    stock_graph(st.session_state.ticker, start_date, end_date)

    # Prepare top_companies data
    yf_service = YahooFinance()
    top_companies_data = {
        c: yf_service.get_stock_data(
            c,
            start=start_date.strftime('%Y-%m-%d'),
            end=end_date.strftime('%Y-%m-%d')
        )
        for c in top_companies
    }

    # Sentiment
    st.write("## Sentiment Analysis")
    ticker_obj = yf.Ticker(st.session_state.ticker)
    news_data = ticker_obj.get_news()

    stock_data = get_stock_data(
        st.session_state.ticker,
        start=start_date.strftime('%Y-%m-%d'),
        end=end_date.strftime('%Y-%m-%d'),
        interval="1d"
    )
    
    sentiment_analyzer = SentimentAnalyzer()
    sentiment = sentiment_analyzer.analyze_sentiment_from_json(news_data)

    if sentiment == 'Positive':
        sentiment_score = 1.0
        sentiment_color = "green"
    elif sentiment == 'Neutral':
        sentiment_score = 0.5
        sentiment_color = "yellow"
    else:
        sentiment_score = 0.1
        sentiment_color = "red"

    st.markdown(f"""
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <span>{"<b style='font-size: 1.5em;'>Negative</b>" if sentiment == 'Negative' else "Negative"}</span>
            <span>{"<b style='font-size: 1.5em;'>Neutral</b>" if sentiment == 'Neutral' else "Neutral"}</span>
            <span>{"<b style='font-size: 1.5em;'>Positive</b>" if sentiment == 'Positive' else "Positive"}</span>
        </div>
        """, unsafe_allow_html=True)

    st.markdown(f"""
        <style>
        .stProgress > div > div > div > div {{
            background-color: {sentiment_color} !important;
        }}
        .stProgress > div > div > div > div {{
            background-color: {sentiment_color} !important;
        }}
        </style>
        """, unsafe_allow_html=True)
    st.progress(sentiment_score)

    # Conversation messages
    st.write("## Chat History")

    # For each user or assistant msg, display in the correct bubble
    for msg in st.session_state["messages"]:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    if user_input:
        
        system_prompt = (
            f"Answer my questions based on the {st.session_state.ticker} stock data given here: {stock_data} and news data given here: {news_data}. Ensure that your answers are thorough by properly referencing the recent data provided."
        )

        # Stream assistant reply once in this column
        with st.chat_message("assistant"):
            assistant_reply = chatbot(system_prompt, st.session_state["messages"])

        # Store new assistant message into st.session_state
        st.session_state["messages"].append({"role": "assistant", "content": assistant_reply})

# ----------------------------------------
# RIGHT COLUMN
# ----------------------------------------
with detail_col:
    st.header("Top Companies")
    for company in top_companies:
        data = top_companies_data.get(company)
        if data is None or data.empty:
            continue

        last_close = round(data["Close"].iloc[-1], 2)
        first_close = data["Close"].iloc[0]
        pct_change = round((last_close - first_close) / first_close * 100, 2)

        st.write(
            f"""
            <div class="stock-cards" style="
                border-radius: 10px; 
                padding: 10px 14px; 
                background-color: rgb(38, 39, 48);
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
                    <a class="stock-details" target="_self" 
                       href="/ticker?name={company}&startDate={start_date}&endDate={end_date}" style="
                       text-decoration: none; 
                       color: inherit;
                       padding: 3px 12px;
                       border-radius: 10px;
                       height: 40px;
                       align-items: center;
                       display: flex;
                       background-color: rgb(63 64 71);">
                       View Details
                    </a>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    # ----------------------------------
    # NEWS SECTION
    # ----------------------------------
    st.header("Latest News")

    st.markdown(
        """
        <style>
        .news-box {
            border-radius: 10px;
            padding: 10px;
            margin-bottom: 15px; 
            overflow: hidden;
            display: flex;
            flex-direction: row;
            background-color: rgb(38, 39, 48);
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
        </style>
        """,
        unsafe_allow_html=True
    )

    for news_item in news_data:
        content = news_item['content']
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
