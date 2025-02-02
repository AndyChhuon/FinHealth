import streamlit as st
import pandas as pd
from io import StringIO
from modules.chatbot_analysis import chatbot_analysis

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
                <a class="sidebar-url" href="http://localhost:8501/portfolio_analysis" target="_self" style="text-decoration: none; color: white; width: 100%;">
                Portfolio
            </a>
            </div>
            """,
            unsafe_allow_html=True
    )

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
    """, unsafe_allow_html=True
)

st.header('Portfolio Analysis')

import io
import streamlit as st
from PIL import Image

# Upload an image
uploaded_file = st.file_uploader("Upload An Image")
img = None

if uploaded_file is not None:
    # Read the file as bytes (binary)
    bytes_data = uploaded_file.getvalue()

    # Convert bytes to an image using PIL
    img = Image.open(io.BytesIO(bytes_data))

    # Display the image (optional)
    st.image(img, caption='Uploaded Image', use_container_width=True)

# Assuming you want to send this image to the chatbot for analysis
if uploaded_file:
    chatbot_analysis("""
    Act as I send you an image of my portfolio with the following details
Portfolio

CASH:
  Shares: 59.7472
  Total value: $2,987.36 CAD
  Change: -$3.59 (-0.12%)

QQC:
  Shares: 40
  Total value: $1,483.20 CAD
  Change: +$24.80 (+1.70%)

XEQT:
  Shares: 446.3044
  Total value: $15,674.21 CAD
  Change: +$1,967.62 (+14.36%)

now describe my portfolio and give advice and analyze it
    """, True)