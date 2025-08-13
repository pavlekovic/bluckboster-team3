import pandas as pd
from sqlalchemy import create_engine
import streamlit as st
import plotly.graph_objects as go

## --------------------------------------- READ FROM CSV ---------------------------------------

# Load the CSV file - it runs faster (comment out the sql part for now)
df_loaded = pd.read_csv("output.csv")

# Preview the result of csv
df_loaded.info()

def display_ratings():
    st.header("Rank movies by rental frequency")
    # Create ratings filter
    f1_ratings_all = df_loaded["rating"].dropna() # Remove NAs
    f1_unique_ratings = f1_ratings_all.unique() # Get unique
    f1_ratings = sorted(list(f1_unique_ratings)) # Create ratings list and sort
    
    # Drop down menu for ratings (multiselect)
    f1_selected_ratings = st.multiselect(
        "Filter by rating",
        options=f1_ratings
        #default=None
    )

	# Create category filter
    f1_categories_all = df_loaded["category_name"].dropna() # Remove NAs
    f1_unique_categories = f1_categories_all.unique() # Get unique
    f1_categories = sorted(list(f1_unique_categories)) # Create category list and sort
    
    # Drop down menu for categories (selectbox)
    f1_selected_category = st.selectbox(
        "Choose a category",
        options=f1_categories,
        index=None
    )

	# Create number of results filter (slider)
    f1_top_n = st.slider("Show Top N titles", min_value=5, max_value=50, value=10, step=1)

    # Filter by ratings and category
    f1_filtered = df_loaded.copy() # Create a copy of data
    
    f1_filtered = f1_filtered[f1_filtered["rating"].isin(f1_selected_ratings)]
    f1_filtered = f1_filtered[f1_filtered["category_name"] == f1_selected_category]

    # Count rentals (count rental_ids)
    # Drop rows where rental_id is null to avoid counting non-rented films
    f1_ranked = (
        f1_filtered.dropna(subset=["rental_id"]) # Remove non-rented films
        .groupby("title", as_index=False)["rental_id"] # Aggregate
        .count() # Count
        .rename(columns={"rental_id": "rental_count"})
        .sort_values("rental_count", ascending=False) # Descending
        .head(f1_top_n)
    )
    
    # Sort results
    f1_ranked = f1_ranked.sort_values(by="rental_count", ascending=False)
    
    # Display only if filters selected
    if f1_selected_ratings and f1_selected_category:

		# Display graph
        f1_fig = go.Figure()
        f1_fig.add_trace(go.Bar(
    	x=f1_ranked['title'],
    	y=f1_ranked['rental_count'],
    	))
        
        f1_fig.update_layout(
        barmode='group',
        title=f"Top {min(f1_top_n, len(f1_ranked))} in category '{f1_selected_category}'",
        xaxis_title='Title',
        yaxis_title='Rental count',
        xaxis_tickangle=-45,
        showlegend=False
    	)
        
        st.plotly_chart(f1_fig)
        
        # Table with results
        st.dataframe(f1_ranked, use_container_width=True)