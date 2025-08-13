import pandas as pd
from sqlalchemy import create_engine
import streamlit as st
import plotly.graph_objects as go

# Logo
st.sidebar.image("images/Logo.png", width=300)

# Title
st.sidebar.title("BluckBoster")

# Add some explanatory text
st.sidebar.markdown("Explore the options and find your next bluckboster!")


## --------------------------------------- LOAD FROM DB ---------------------------------------


# Connection details
#DB_HOST = 'data-sandbox.c1tykfvfhpit.eu-west-2.rds.amazonaws.com'
#DB_PORT = '5432'
#DB_NAME = 'pagila'
#DB_SCHEMA = 'main'
#DB_USER = 'de13_repa'  # replace with actual username from noodle
#DB_PASS = 'Cb3EfSoG'  # replace with actual password from noodle

# Create engine
#engine = create_engine(
#    f'postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}')

# Define the SQL query 
# - we might need to reduce the table, but this is most of the informaion
# query = f"""
# SELECT 
# 	f.film_id,
# 	f.title,
# 	f.description,
# 	f.release_year,
# 	f.language_id,
# 	f.rental_duration,
# 	f.rental_rate,
# 	f."length",
# 	f.replacement_cost,
# 	f.rating,
# 	f.last_update AS "last_film_update",
# 	f.special_features,
# 	f.fulltext,
# 	l."name" AS "language",
# 	l.last_update AS "last_language_update",
# 	i.inventory_id,
# 	i.store_id,
# 	i.last_update AS "last_inventory_update",
# 	a.first_name AS "actor_first_name",
# 	a.last_name AS "actor_last_name",
# 	cat."name" AS "category_name",
# 	r.rental_id,
# 	r.rental_date,
# 	r.customer_id,
# 	r.return_date,
# 	r.staff_id,
# 	r.last_update AS "last_rental_update",
# 	p.payment_id,
# 	p.amount,
# 	p.payment_date,
# 	cust.store_id,
# 	s.address_id AS "store_address_id",
# 	addr.address AS "store_address",
# 	addr.address2 AS "store_address2",
# 	addr.district AS "store_district",
# 	addr.city_id AS "store_city_id",
# 	addr.postal_code AS "store_postal_code",
# 	addr.phone AS "store_phone",
# 	addr.last_update AS "last_store_address_update",
# 	city.city AS "store_city",
# 	city.country_id AS "store_country_id",
# 	city.last_update AS "last_store_city_update",
# 	country.country AS "store_country",
# 	country.last_update AS "last_store_country_update"
# FROM main.film AS f
# LEFT JOIN main."language" AS l
# ON l.language_id = f.language_id
# LEFT JOIN inventory AS i
# ON i.film_id = f.film_id
# LEFT JOIN film_actor AS fa 
# ON fa.film_id = f.film_id 
# LEFT JOIN actor AS a 
# ON a.actor_id = fa.actor_id
# LEFT JOIN film_category AS fc 
# ON fc.film_id = f.film_id 
# LEFT JOIN category AS cat 
# ON cat.category_id = fc.category_id 
# LEFT JOIN rental AS r 
# ON r.inventory_id = i.inventory_id 
# LEFT JOIN payment AS p
# ON p.rental_id = r.rental_id 
# LEFT JOIN customer AS cust
# ON cust.customer_id = r.customer_id 
# LEFT JOIN store AS s 
# ON s.store_id = cust.store_id 
# LEFT JOIN address AS addr 
# ON s.address_id = addr.address_id 
# LEFT JOIN city 
# ON city.city_id = addr.city_id 
# LEFT JOIN country 
# ON country.country_id = city.country_id;
#
# # Load into DataFrame
# df = pd.read_sql_query(query, con=engine)
#
# # Preview the result
# df.info()
#
# # Save the DataFrame to a CSV 
# # (You can't leave your user name and password on here, unless you don't mind!)
# df.to_csv("output.csv", index=False)


## --------------------------------------- READ FROM CSV ---------------------------------------


# Load the CSV file - it runs faster (comment out the sql part for now)
df_loaded = pd.read_csv("output.csv")

# Preview the result of csv
df_loaded.info()


## --------------------------------------- STREAMLIT APP ---------------------------------------

# Create tabs
tab_homepage, tab_ratings, tab_actors, tab_film_details  = st.tabs(["Homepage", "Ratings", "Actors", "Film details"])

# Page 1 - Welcome Page (low priority) - brief intro plus link to README (if we eventually make a Readme)

# with tab_homepage:

# Page 2 - Rank movies in each category based on frequency of rental (count rental ids)
# - include filter for rating (E.G PG rated)

# Content for tab 2
with tab_ratings:
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

# Page 4 - Filter by actor 
# - show films the actor was in
# Filter by category and/or year and/or rating\

# Content for tab 3
with tab_actors:
    
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


# Page 3 - Search for a film and get details of that film (rating, year, actors, availability, etc)
# Is the movie currently available for rental?
# Which district, city, and country can I find it in?
# If not, maybe recommend renting from a different district, 
# or Recommend a similar movie 
# or suggest wait time.

# Content for tab 4
with tab_film_details:
    
    st.header("Search for an Actor/Actress")
    
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

# Page 5 - EXTRA - Can also generate a movie recommendation 
# ------ based on preferred actor 
# ------ and/or category 
# ------ and/or year
# ------ and/and or rating (E.G PG rated)
# State where the movie can be rented from