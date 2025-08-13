import os
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv

# Load variables from .env into process environment
load_dotenv()

# Read env vars (fail early if something is missing)
required = ["DB_HOST", "DB_PORT", "DB_NAME", "DB_USER", "DB_PASS"]
missing = [k for k in required if not os.getenv(k)]
if missing:
    raise RuntimeError(f"Missing required env vars: {', '.join(missing)}")

DB_HOST   = os.getenv("DB_HOST")
DB_PORT   = os.getenv("DB_PORT")
DB_NAME   = os.getenv("DB_NAME")
DB_USER   = os.getenv("DB_USER")
DB_PASS   = os.getenv("DB_PASS")

# Create engine
engine = create_engine(
    f'postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
)

# Define the SQL query
# - we might need to reduce the table, but this is most of the information
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
    ON country.country_id = city.country_id;
"""

# Load into DataFrame
df = pd.read_sql_query(query, con=engine)

# Preview the result
df.info()

# Save the DataFrame to a CSV 
# (You can't leave your username and password in the code if you share it publicly!)
df.to_csv("output.csv", index=False)