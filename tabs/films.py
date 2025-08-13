import pandas as pd
from sqlalchemy import create_engine
import streamlit as st
import plotly.graph_objects as go

## --------------------------------------- READ FROM CSV ---------------------------------------

# Load the CSV file - it runs faster (comment out the sql part for now)
df_loaded = pd.read_csv("output.csv")

# Preview the result of csv
df_loaded.info()

def display_film_details():
    
    st.header("Search for film details")
    
    # Movie and city selection
    movies = df_loaded['title'].dropna().drop_duplicates().sort_values().tolist()
    selected_title = st.selectbox(
        "Select a movie",
        movies,
        index=None)

    cities = df_loaded['store_city'].dropna().drop_duplicates().sort_values().tolist()
    selected_city = st.selectbox(
        "Select a city",
        cities,
        index=None)

    # Filter for selected city and movie
    city_movie_df = df_loaded[
        (df_loaded['store_city'] == selected_city) &
        (df_loaded['title'] == selected_title)
    ]

    if selected_title and selected_city:
        if not city_movie_df.empty:
            # Check availability per store
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

            # Show availability per store
            st.text(f"Availability in {selected_city}:")
            store_availability = city_movie_df.groupby('store_id')['available'].any()
            for store_id, available in store_availability.items():
                status = "Available" if available else "Not Available"
                st.text(f"Store {int(store_id)}: {status}")

            # Suggest similar movies if not available
            if not is_available:
                st.warning("This movie is currently not available. Here are some suggestions:")
                selected_movie_row = city_movie_df.iloc[0]

                suggestions = df_loaded[
                    (df_loaded['title'] != selected_title) &
                    (df_loaded['category_name'] == selected_movie_row['category_name']) &
                    (df_loaded['rating'].between(selected_movie_row['rating'] - 0.5,
                                                selected_movie_row['rating'] + 0.5))
                ]['title'].drop_duplicates().tolist()

                if suggestions:
                    for movie in suggestions[:5]:  # show up to 5 suggestions
                        st.text(f"- {movie}")
                else:
                    st.text("No similar movies available.")
        else:
            st.text(f"The movie '{selected_title}' is not available in {selected_city}.")