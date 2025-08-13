# run -  pip install sqlalchemy psycopg2 pandas

import pandas as pd
from sqlalchemy import create_engine
import streamlit as st

# Connection details
DB_HOST = 'data-sandbox.c1tykfvfhpit.eu-west-2.rds.amazonaws.com'
DB_PORT = '5432'
DB_NAME = 'pagila'
DB_SCHEMA = 'main'
DB_USER = 'user'  # replace with actual username from noodle
DB_PASS = 'pass'  # replace with actual password from noodle

# Create engine
engine = create_engine(
    f'postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
)

# Define the SQL query 
# - we might need to reduce the table, but this is most of the informaion
query = f"""
    SELECT 
        f.film_id,
        f.title,
        f.description,
        f.release_year,
        f.language_id,
        f.rental_duration,
        f.rental_rate,
        f."length",
        f.replacement_cost,
        f.rating,
        f.last_update AS "last_film_update",
        f.special_features,
        f.fulltext,
        l."name" AS "language",
        l.last_update AS "last_language_update",
        i.inventory_id,
        i.store_id,
        i.last_update AS "last_inventory_update",
        a.first_name AS "actor_first_name",
        a.last_name AS "actor_last_name",
        cat."name" AS "category_name",
        r.rental_id,
        r.rental_date,
        r.customer_id,
        r.return_date,
        r.staff_id,
        r.last_update AS "last_rental_update",
        p.payment_id,
        p.amount,
        p.payment_date,
        cust.store_id,
        s.address_id AS "store_address_id",
        addr.address AS "store_address",
        addr.address2 AS "store_address2",
        addr.district AS "store_district",
        addr.city_id AS "store_city_id",
        addr.postal_code AS "store_postal_code",
        addr.phone AS "store_phone",
        addr.last_update AS "last_store_address_update",
        city.city AS "store_city",
        city.country_id AS "store_country_id",
        city.last_update AS "last_store_city_update",
        country.country AS "store_country",
        country.last_update AS "last_store_country_update"
    FROM main.film AS f
    LEFT JOIN main."language" AS l
    ON l.language_id = f.language_id
    LEFT JOIN inventory AS i
    ON i.film_id = f.film_id
    LEFT JOIN film_actor AS fa 
    ON fa.film_id = f.film_id 
    LEFT JOIN actor AS a 
    ON a.actor_id = fa.actor_id
    LEFT JOIN film_category AS fc 
    ON fc.film_id = f.film_id 
    LEFT JOIN category AS cat 
    ON cat.category_id = fc.category_id 
    LEFT JOIN rental AS r 
    ON r.inventory_id = i.inventory_id 
    LEFT JOIN payment AS p
    ON p.rental_id = r.rental_id 
    LEFT JOIN customer AS cust
    ON cust.customer_id = r.customer_id 
    LEFT JOIN store AS s 
    ON s.store_id = cust.store_id 
    LEFT JOIN address AS addr 
    ON s.address_id = addr.address_id 
    LEFT JOIN city 
    ON city.city_id = addr.city_id 
    LEFT JOIN country 
    ON country.country_id = city.country_id 
    ;
"""

# Load into DataFrame
#df = pd.read_sql_query(query, con=engine)

# Preview the result
#df.info()

# Save the DataFrame to a CSV 
# (You can't leave your user name and password on here, unless you don't mind!)
#df.to_csv("output.csv", index=False)


# Load the CSV file - it runs faster (comment out the sql part for now)
df_loaded = pd.read_csv("output.csv")

# Preview the result of csv
df_loaded.info()


## Streamlit section
# Create tabs for each page
page1_tab, page2_tab, page3_tab, page4_tab = st.tabs(["Welcome Page", "Movies Rank", "Film details", "Search by actor"])

# Page 1 - Welcome Page (low priority) - brief intro plus link to README (if we eventually make a Readme)
with page1_tab:
    st.header("Welcome to Bluckbosters!")

# Page 2 - Rank movies in each category based on frequency of rental (count rental ids)
# - include filter for rating (E.G PG rated)
with page2_tab:
    st.header("Rank of movies!")


# Page 3 - Search for a film and get details of that film (rating, year, actors, availability, etc)
# Is the movie currently available for rental?
# Which distrit, city, and country can I find it in?
# If not, maybe recommend renting from a different district, 
# or Recommend a similar movie 
# or suggest wait time.
with page3_tab:
    st.header("More about your favourite movie!")


# Page 4 - Filter by actor 
# - show films the actor was in
# Filter by category and/or year and/or rating 
with page4_tab:
    st.header("More about your favourite actor!")
    page4_df = df_loaded.copy()

    page4_df["actor_full_name"] = (
        page4_df["actor_first_name"].fillna("") + " " + page4_df["actor_last_name"].fillna("")
    ).str.strip()

    page4_df = page4_df[page4_df["actor_full_name"].str.strip() != ""]

    # Sidebar filters
    st.title("Filter by Actor Name")

    # Actor name filter
    page4_actor_names = sorted(page4_df["actor_full_name"].dropna().unique())
    page4_selected_actor = st.selectbox("Select Actor Name", page4_actor_names, index=0)

    # Rating filter
    page4_ratings = sorted(page4_df["rating"].dropna().unique())
    page4_selected_ratings = st.multiselect("Select Rating", page4_ratings, default=page4_ratings)

    # Category filter
    page4_categories = sorted(page4_df["category_name"].dropna().unique())
    page4_selected_categories = st.multiselect("Select Category", page4_categories, default=page4_categories)

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


#    page4_display_df = page4_filtered_df[["title", 
#                                          "release_year", 
#                                          "length", 
#                                          "rating", 
#                                          "language", 
#                                          "category_name"]]


    page4_grouped_df.rename(columns={
                        "title": "Title",
                        "release_year": "Year",
                        "length": "Length (mins)",
                        "rating": "Rating",
                        "category_name": "Category",
                        "language": "Language"
                    }, inplace=True)

    # Display results
    st.subheader("List of Movies they've been in:")
    st.dataframe(page4_grouped_df.reset_index(drop=True))

# Page 5 - EXTRA - Can also generate a movie recommendation 
#  ---- based on preffered actor 
# ------ and/or category 
# ------ and/or year
# ------ and/and or rating (E.G PG rated)
# State where the movie can be rented from