import streamlit as st
from datetime import datetime, timedelta
# from services.yahoofinance import YahooFinance
import yfinance as yf
from services.sentimentAnalyzer import SentimentAnalyzer
from modules.chatbot import chatbot
from modules.stock_graph import stock_graph, get_stock_data

with st.sidebar:
    st.logo("assets/chart_icon.png")
    st.html(
        ""
    )
    st.page_link(page='http://localhost:8501/', label="Home")
    st.page_link(page='http://localhost:8501/analysis', label="Personal Analysis")

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
        width: 220px;
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
    </style>
    """, unsafe_allow_html=True
)
st.title('Ticker Details')

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

    # # Fetch and display stock data
    stock_data = get_stock_data(ticker, start=start_date.strftime('%Y-%m-%d'), end=end_date.strftime('%Y-%m-%d'), interval="1d")
    # st.write(f"## {ticker} Stock Data")
    # st.line_chart(stock_data['Close'])

    stock_graph(symbol=ticker, start=start_date, end=end_date, )

    # Fetch news regarding data and display
    ticker_obj = yf.Ticker(ticker)
    news_data = ticker_obj.get_news()
    st.write(f"## {ticker} News")

    # Sentiment analysis
    st.write("## Sentiment Analysis")
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
        <div style="display: flex; justify-content: space-between;">
            <span>{"<b style='font-size: 1.5em;'>😢 Negative</b>" if sentiment == 'Negative' else "😢 Negative"}</span>
            <span>{"<b style='font-size: 1.5em;'>😐 Neutral</b>" if sentiment == 'Neutral' else "😐 Neutral"}</span>
            <span>{"<b style='font-size: 1.5em;'>😊 Positive</b>" if sentiment == 'Positive' else "😊 Positive"}</span>
        </div>
        """, unsafe_allow_html=True)
    st.markdown(f"""
        <style>
        .st-c6 > .st-cb {{
            background-color: {sentiment_color} !important;
        }}
        .st-c6 > .st-cr {{
            background-color: {sentiment_color} !important;
        }}
        </style>
        """, unsafe_allow_html=True)
    st.progress(sentiment_score)

    # Responsive grid for news 
    st.markdown(
        """
        <style>
        .news-box {
            border: 1px solid #e6e6e6;
            border-radius: 10px;
            padding: 10px;
            margin-bottom: 15px; 
            height: 380px; 
            overflow: hidden;
            display: flex;
            flex-direction: column;
            background-color: #1e1e1e;
        }
        .news-box img {
            border-radius: 10px;
            height: 150px;
            object-fit: cover;
        }
        .news-box h3 {
            color: white;
            font-size: 1.1em;
            margin: 0;
            line-height: 1.2; 
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
        .stHorizontalContainer {
            display: flex;
            flex-wrap: wrap; 
            justify-content: space-between; 
        }
        .stMarkdownContainer {
            padding: 0;
        }
        .stHorizontalContainer {
            display: flex;
            flex-wrap: wrap; 
            justify-content: space-between; 
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    # Display in 3 columns
    for i in range(0, len(news_data), 3):
        cols = st.columns(3)
        for col, news in zip(cols, news_data[i:i+3]):
            content = news['content']
            # Check if there is no image 
            thumbnail_url = content['thumbnail']['resolutions'][0]['url'] if content['thumbnail'] else None
            title = content['title']
            summary = content['summary']
            link = content['canonicalUrl']['url']
            with col:
                st.markdown(
                    f"""
                    <a href="{link}" target="_blank" style="text-decoration: none;">
                        <div class="news-box">
                            <img src="{thumbnail_url}" style="width: 100%;">
                            <h3>{title}</h3>
                            <p>{summary}</p>
                        </div>
                    </a>
                    """,
                    unsafe_allow_html=True
                )
                
else:
    st.write("No ticker selected.")

chatbot(f"Answer my questions based on the {ticker} stock data given here: {stock_data} and news data given here: {news_data}")