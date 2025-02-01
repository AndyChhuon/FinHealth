import streamlit as st

st.title('🎈 App Name test')

st.write('Hello world!')

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