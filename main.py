import streamlit as st
from tabs.homepage import display_homepage
from tabs.ratings import display_ratings
from tabs.actors import display_actors
from tabs.films import display_film_details

# Logo
st.sidebar.image("images/logo.png", width=300)

# Title
st.sidebar.title("BluckBoster")

# Add some explanatory text
st.sidebar.markdown("Explore the options and find your next bluckboster!")



## --------------------------------------- STREAMLIT APP ---------------------------------------

def main():
    # ---------- Page config ----------
    st.set_page_config(
        page_title="BluckBoster",
        page_icon="🎬",
        layout="wide"
    )

    # Main-page tabs instead of sidebar
    tab1, tab2, tab3, tab4 = st.tabs(["Homepage", "Ratings", "Actors", "Film details"])

    with tab1:
        display_homepage()

    with tab2:
        display_ratings()

    with tab3:
        display_actors()

    with tab4:
        display_film_details()

if __name__ == "__main__":
    main()