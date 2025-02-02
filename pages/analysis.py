import streamlit as st

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
                Personal Analysis
            </a>
            </div>
            """,
            unsafe_allow_html=True
        )
    #st.page_link(page='http://localhost:8501/', label="Home")
    #st.page_link(page='http://localhost:8501/analysis', label="Personal Analysis")

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
st.title('Personal Analysis')