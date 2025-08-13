# BluckBoster — Movie Rental Analytics App

**BluckBoster** is a Streamlit-based analytics app for exploring movie rental data from the **Pagila** sample database.  
It was created by **Abdullah**, **Comfort**, **Luke**, **Renato**, and **Sahil**.

---

## How the App Works

1. **Load data from Pagila database**  
   - The app connects to the Pagila PostgreSQL database.
   - It joins all relevant tables to make sure we have a **complete dataset** containing films, rentals, actors, categories, stores, and payments.
   - The joined dataset is loaded into a **pandas DataFrame**.

2. **Export to CSV for faster reloads**  
   - After the initial load, the DataFrame is exported to a CSV file.
   - On subsequent runs, the app can load data directly from this CSV instead of re-querying the database — speeding up load times.

---

## Pagila Database Schema

Below is a simplified diagram showing how the tables are joined to produce the final dataset:

![main ERD](./images/mainERD.png)

---

## Pages in the App

The app contains **four main pages**:

1. **Homepage**  
   - Displays basic information about the app.
   - Includes a retro-themed GIF for a nostalgic touch.

2. **Ratings Page**  
   - Lets you see the **top rented movies**.
   - Supports **filters** by category (genre) and rating (e.g., G, PG, PG-13, R).

3. **Actors Page**  
   - Shows all movies an actor has appeared in.
   - Supports **filters** by rating and genre.
   - Useful for exploring an actor’s filmography within the rental dataset.

4. **Film Details Page**  
   - Displays **further details** for a selected film, including:
     - Description
     - Rental price
     - Language
     - Store availability
     - Other metadata

---

## Tech Stack

- **Python** (pandas, SQLAlchemy)
- **PostgreSQL** (Pagila sample DB)
- **Streamlit** (web app framework)

---

## Running the App

1. Create and activate a virtual environment:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate  # macOS/Linux
   # .venv\Scripts\activate   # Windows
   pip install -r requirements.txt
   streamlit run main.py

---

# User Stories & Acceptance Criteria

## 1. Search for a Movie by Title
**As a** movie rental customer  
**I want to** search for a movie by title  
**So that** I can quickly find the film I want to rent  

**Acceptance Criteria:**
- User can type a movie title into a search box.
- Matching movies are displayed **as the user types** or **after clicking Search**.
- Search results show **unique movie titles** without duplicates.

---

## 2. Filter Movies by City
**As a** movie rental customer  
**I want to** select a city when searching for a movie  
**So that** I only see availability for stores near me  

**Acceptance Criteria:**
- A dropdown or input field allows the user to **select a city**.
- The list of available movies updates to reflect the chosen city.
- If no city is selected, all movies are shown by default.

---

## 3. View Detailed Movie Information
**As a** movie rental customer  
**I want to** see the details of a selected movie including rating, runtime, release year, description, language, category, and price  
**So that** I can decide if it is the right choice for me  

**Acceptance Criteria:**
- When a movie is selected, **all details are displayed** in a structured format.
- Price is shown with the **£ symbol** before the amount.
- All data fields appear even if some values are missing (placeholders used where necessary).

---

## 4. Notify When Movie is Not Available
**As a** movie rental customer  
**I want to** be informed if the movie I want is not available in my city  
**So that** I can choose another film instead of waiting  

**Acceptance Criteria:**
- If the selected movie is unavailable in the chosen city, a message clearly states:  
  `"Not Available in Your City"`.
- The availability check is based on **rental and return dates** for that city’s stores.
- The message is visually distinct so it cannot be missed.

---

## 5. Suggest Alternatives When Movie is Unavailable
**As a** movie rental customer  
**I want to** receive alternative movie suggestions when my chosen movie is unavailable  
**So that** I can still find a similar movie to watch  

**Acceptance Criteria:**
- Suggestions are based on **matching category** and **similar rating** (+/- 1 point).
- At least **3 alternative movies** are displayed when possible.
- Each suggestion includes **title**, **rating**, and **availability** in the chosen city.

---

## 6. Search for Movies by Actor
**As a** movie rental customer  
**I want to** search for movies by an actor’s name  
**So that** I can find and rent films featuring my favorite performers  

**Acceptance Criteria:**
- User can type an **actor’s name** into a search box.
- Search results display **all movies** in the database featuring that actor.
- Results show **movie title**, **release year**, and **availability** in the selected city.
- If no matches are found, a clear `"No movies found"` message is displayed.