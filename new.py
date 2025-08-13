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


col1, col2 = st.columns(2)

rows = df_loaded[df_loaded["title"] == selected]

year = int(rows["release_year"].dropna().iloc[0])
lang = rows["language"].dropna().iloc[0]
rating = rows["rating"].dropna().iloc[0]
cats = rows["category_name"].dropna().iloc[0]
with col1:
    st.markdown(
        f"""
        <div style='text-align:left; font-size:18px; line-height:1.4;'>
            <b>Year:</b> {year}<br>
            <br>
            <b>Language:</b> {lang}
        </div>
        """,
        unsafe_allow_html=True,
    )

with col2:
    st.markdown(
        f"""
        <div style='text-align:left; font-size:18px; line-height:1.4;'>
            <b>Rating:</b> {rating}<br>
            <br>
            <b>Categories:</b> {cats}
        </div>
        """,
        unsafe_allow_html=True,
    )
