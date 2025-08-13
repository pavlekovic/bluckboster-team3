import pandas as pd
from sqlalchemy import create_engine
import streamlit as st
import plotly.graph_objects as go

## --------------------------------------- READ FROM CSV ---------------------------------------

# Load the CSV file - it runs faster (comment out the sql part for now)
df_loaded = pd.read_csv("extract/output.csv")

# Preview the result of csv
df_loaded.info()


def display_homepage():
    
    # Title and intro
    st.title("Welcome to BluckBoster")
    
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        st.image("images/vhs.gif")   
    
    # Description
    st.write(
        """
        **BluckBoster** is an app for those who long for simpler times when family fun 
        was renting out movies from a local store.  

        It is designed to explore movie rental data, providing insights into rentals, 
        revenue, categories, and more.
        """
    )

    # Team credits
    st.subheader("Created by:")
    st.write(
        """
        - Abdullah  
        - Comfort  
        - Luke  
        - Renato  
        - Sahil
        """
    )