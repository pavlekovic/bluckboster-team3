import streamlit as st
import pandas as pd
from main import df_loaded


st.image("images/Logo.png", width=220)

# centered title
st.markdown("""<style> h1 {text-align: center;} </style>""", unsafe_allow_html=True)

st.title("BluckBoster")


titles = (
    df_loaded["title"]
    .dropna()
    .astype(str)
    .drop_duplicates()
    .sort_values()
    .tolist()
)

selected = st.selectbox("Search for movie:", options=titles)