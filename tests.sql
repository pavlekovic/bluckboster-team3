-- Check distinct count of realease_year, rating, and film_id
SELECT 
	COUNT(DISTINCT release_year) AS distinct_year_count,
	COUNT(DISTINCT rating) AS DC_RATINGS,
	COUNT(DISTINCT film_id) AS DC_movies
FROM film;

-- Check distint count of category
SELECT COUNT(DISTINCT "name") AS DC_category
FROM category;

-- Check distinct count of actor_id, subtract 1 for the empty actor in the join
SELECT COUNT(DISTINCT actor_id) AS DC_actor_id
FROM actor;

-- Check distinct count of store_id, city_id, and country_id
SELECT 
	COUNT(DISTINCT s.store_id) AS DC_store,
	COUNT(DISTINCT city.city_id) AS DC_city,
	COUNT(DISTINCT country.country_id) AS DC_country
FROM store AS s
LEFT JOIN address AS addr 
ON s.address_id = addr.address_id 
LEFT JOIN city 
ON city.city_id = addr.city_id 
LEFT JOIN country 
ON country.country_id = city.country_id 
;
