import pandas as pd

## --------------------------------------- READ FROM CSV ---------------------------------------

# Load the CSV file - it runs faster (comment out the sql part for now)
try:
    file = "output.csv"
    df_loaded = pd.read_csv(file)
    print(f"Passed: {file} was successfully loaded!")
except:
    print(f"Failed: {file} failed to load!")

## --------------------------------------- STREAMLIT APP ---------------------------------------

# Create ratings filter
f1_unique_ratings = df_loaded["rating"].dropna().unique() 
f1_ratings = len(list(f1_unique_ratings)) # Count of ratings

try:
    assert f1_ratings == 5
    print("Passed: unique ratings successful!")
except:
    print("Failed: incorrect number of unique ratings!")
    print(f1_ratings, " != 5")


# Create category filter
f1_unique_categories = df_loaded["category_name"].dropna().unique() 
f1_categories = len(list(f1_unique_categories)) 

try:
    assert f1_categories == 16
    print("Passed: unique categories successful!")
except:
    print("Failed: incorrect number of unique categories!") 
    print(f1_categories , " != 16")

# Actor name filter
page4_df = df_loaded.copy()

page4_df["actor_full_name"] = (
        page4_df["actor_first_name"].fillna("") + " " + page4_df["actor_last_name"].fillna("")
    ).str.strip()

page4_df = page4_df[page4_df["actor_full_name"].str.strip() != ""]

page4_actor_names = sorted(page4_df["actor_full_name"].dropna().unique())
try:
    assert len(page4_actor_names) == 199
    print("Passed: Count of unique actor names successful!")
except:
    print("Failed: incorrect number of actor names!") 
    print(len(page4_actor_names) , " != 199")

# Content for tab 4

# Movie and city selection
movies = df_loaded['title'].dropna().drop_duplicates().tolist()
count_of_movies = len(movies)
try:
    assert count_of_movies == 1000
    print("Passed: Count of movies successful!")
except:
    print("Failed: incorrect number of movies!") 
    print(count_of_movies, " != 1000")

cities = df_loaded['store_city'].dropna().drop_duplicates().tolist()
count_of_cities = len(cities)
try:
    assert count_of_cities == 2
    print("Passed: Count of cities successful!")
except:
    print("Failed: incorrect number of cities!") 
    print(count_of_cities, " != 2")

countries = df_loaded['store_country'].dropna().drop_duplicates().tolist()
count_of_countries = len(countries)
try:
    assert count_of_countries == 2
    print("Passed: Count of countries successful!")
except:
    print("Failed: incorrect number of countries!") 
    print(count_of_countries , " != 2")

release_year = df_loaded['release_year'].dropna().drop_duplicates().tolist()
count_of_release_year = len(release_year)
try:
    assert count_of_release_year == 1
    print("Passed: Count of release_year successful!")
except:
    print("Failed: incorrect number of release_year!") 
    print(count_of_release_year, " != 1")