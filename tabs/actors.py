import pandas as pd
from sqlalchemy import create_engine
import streamlit as st
import plotly.graph_objects as go

## --------------------------------------- READ FROM CSV ---------------------------------------

# Load the CSV file - it runs faster (comment out the sql part for now)
df_loaded = pd.read_csv("output.csv")

# Preview the result of csv
df_loaded.info()

def display_actors():
    
    st.header("Search for an Actor/Actress")
    
    #st.header("More about your favourite actor!")
    page4_df = df_loaded.copy()

    page4_df["actor_full_name"] = (
        page4_df["actor_first_name"].fillna("") + " " + page4_df["actor_last_name"].fillna("")
    ).str.strip()

    page4_df = page4_df[page4_df["actor_full_name"].str.strip() != ""]

    # Actor name filter
    page4_actor_names = sorted(page4_df["actor_full_name"].dropna().unique())
    page4_selected_actor = st.selectbox(
        "Select Actor Name",
        page4_actor_names,
        index=None)

    # Rating filter
    page4_ratings = sorted(page4_df["rating"].dropna().unique())
    page4_selected_ratings = st.multiselect(
        "Select Rating",
        page4_ratings)

    # Category filter
    page4_categories = sorted(page4_df["category_name"].dropna().unique())
    page4_selected_categories = st.multiselect(
        "Select Category",
        page4_categories)

    # Apply filters
    page4_filtered_df = page4_df[
        (page4_df["actor_full_name"] == page4_selected_actor) &
        (page4_df["category_name"].isin(page4_selected_categories)) &
        (page4_df["rating"].isin(page4_selected_ratings))
    ]

    page4_grouped_df = (
        page4_filtered_df
        .groupby(["title", "release_year", "length", "rating", "language", "category_name"])
        .agg({"actor_full_name": lambda x: ", ".join(sorted(set(x)))})
        .reset_index()
    )

    page4_grouped_df = page4_grouped_df[
        ["title", 
        "release_year", 
        "length", 
        "rating", 
        "language", 
        "category_name"]
    ]

    page4_grouped_df.rename(columns={
        "title": "Title",
        "release_year": "Release Year",
        "length": "Length (mins)",
        "rating": "Rating",
        "category_name": "Category",
        "language": "Language"
        }, inplace=True)

    page4_grouped_df = page4_grouped_df.sort_values(by="Title")


    # Display results
    if page4_selected_actor and page4_selected_ratings and page4_selected_categories:
        st.subheader("List of Movies they've been in:")
        st.dataframe(page4_grouped_df.reset_index(drop=True))