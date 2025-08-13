import pandas as pd
from sqlalchemy import create_engine
import streamlit as st
import plotly.graph_objects as go

## --------------------------------------- READ FROM CSV ---------------------------------------

# Load the CSV file - it runs faster (comment out the sql part for now)
df_loaded = pd.read_csv("extract/output.csv")

# Preview the result of csv
df_loaded.info()

def display_film_details():
    
    st.header("Search for film details")
    
    # Movie and city selection
    movies = df_loaded['title'].dropna().drop_duplicates().sort_values().tolist()
    selected_title = st.selectbox("Select a movie", movies)

    cities = df_loaded['store_city'].dropna().drop_duplicates().sort_values().tolist()
    selected_city = st.selectbox("Select a city", cities)

    # Filter for selected city and movie
    city_movie_df = df_loaded[
        (df_loaded['store_city'] == selected_city) &
        (df_loaded['title'] == selected_title)
    ]

    if not city_movie_df.empty:
        # Check availability per copy
        city_movie_df['available'] = city_movie_df.apply(
            lambda row: pd.isna(row['rental_date']) or pd.notna(row['return_date']),
            axis=1
        )
        is_available = city_movie_df['available'].any()

        # Display movie details
        st.subheader(selected_title)
        st.text(f"Category: {city_movie_df.iloc[0]['category_name']}")
        st.text(f"Rating: {city_movie_df.iloc[0]['rating']}")
        st.text(f"Language: {city_movie_df.iloc[0]['language']}")
        st.text(f"Release Year: {city_movie_df.iloc[0]['release_year']}")
        st.text(f"Description: {city_movie_df.iloc[0]['description']}")
        st.text(f"Price: £{city_movie_df.iloc[0]['amount']}")

        # Show how many copies are available at each store
        store_summary = city_movie_df.groupby('store_address')['available'].agg(['sum', 'count']).reset_index()
        store_summary.rename(columns={'sum': 'available', 'count': 'total'}, inplace=True)

        for i in store_summary.index:
            address = store_summary.loc[i, 'store_address']
            available = int(store_summary.loc[i, 'available'])
            total = int(store_summary.loc[i, 'total'])
            st.text(f"Available copies in {selected_city} - {address}: {available} / {total}")

        # Suggest similar movies if not available
        if not is_available:
            st.warning("This movie is currently not available. Here are some suggestions:")
            selected_movie_row = city_movie_df.iloc[0]

            suggestions = df_loaded[
                (df_loaded['title'] != selected_title) &
                (df_loaded['category_name'] == selected_movie_row['category_name']) &
                (df_loaded['rating'] == selected_movie_row['rating'])
            ]['title'].drop_duplicates().tolist()

            if suggestions:
                for movie in suggestions[:5]:
                    st.text(f"- {movie}")
            else:
                st.text("No similar movies available.")
    else:
        st.text(f"The movie '{selected_title}' is not available in {selected_city}.")