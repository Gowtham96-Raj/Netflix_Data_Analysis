-- Netflix Data Analysis
-- Author: Gowtham Raj S
-- Table name used: netflix_titles

-- 1. View all records
SELECT *
FROM netflix_titles;

-- 2. Count total number of titles
SELECT COUNT(*) AS total_titles
FROM netflix_titles;

-- 3. Count Movies and TV Shows
SELECT type, COUNT(*) AS total_count
FROM netflix_titles
GROUP BY type
ORDER BY total_count DESC;

-- 4. Count titles by country
SELECT country, COUNT(*) AS total_titles
FROM netflix_titles
WHERE country IS NOT NULL
  AND country <> 'Unknown'
GROUP BY country
ORDER BY total_titles DESC
LIMIT 10;

-- 5. Count titles by rating
SELECT rating, COUNT(*) AS total_titles
FROM netflix_titles
WHERE rating IS NOT NULL
  AND rating <> 'Unknown'
GROUP BY rating
ORDER BY total_titles DESC;

-- 6. Count titles by genre
SELECT listed_in AS genre, COUNT(*) AS total_titles
FROM netflix_titles
WHERE listed_in IS NOT NULL
GROUP BY listed_in
ORDER BY total_titles DESC
LIMIT 10;

-- 7. Count titles released each year
SELECT release_year, COUNT(*) AS total_titles
FROM netflix_titles
GROUP BY release_year
ORDER BY release_year DESC;

-- 8. Find titles released after 2020
SELECT title, type, release_year
FROM netflix_titles
WHERE release_year > 2020
ORDER BY release_year DESC;

-- 9. Find all Indian titles
SELECT title, type, release_year, rating
FROM netflix_titles
WHERE country = 'India'
ORDER BY release_year DESC;

-- 10. Find all United States titles
SELECT title, type, release_year, rating
FROM netflix_titles
WHERE country = 'United States'
ORDER BY release_year DESC;

-- 11. Find Drama titles
SELECT title, type, release_year
FROM netflix_titles
WHERE listed_in LIKE '%Drama%'
ORDER BY release_year DESC;

-- 12. Find Comedy titles
SELECT title, type, release_year
FROM netflix_titles
WHERE listed_in LIKE '%Comedy%'
ORDER BY release_year DESC;

-- 13. Find the most recent releases
SELECT title, type, release_year
FROM netflix_titles
ORDER BY release_year DESC
LIMIT 10;

-- 14. Find the oldest releases
SELECT title, type, release_year
FROM netflix_titles
ORDER BY release_year ASC
LIMIT 10;

-- 15. Count titles by director
SELECT director, COUNT(*) AS total_titles
FROM netflix_titles
WHERE director IS NOT NULL
  AND director <> 'Unknown'
GROUP BY director
ORDER BY total_titles DESC
LIMIT 10;

-- 16. Find titles with TV-MA rating
SELECT title, type, country, release_year
FROM netflix_titles
WHERE rating = 'TV-MA'
ORDER BY release_year DESC;

-- 17. Find titles with PG-13 rating
SELECT title, country, release_year
FROM netflix_titles
WHERE rating = 'PG-13'
ORDER BY release_year DESC;

-- 18. Count titles by country and type
SELECT country, type, COUNT(*) AS total_titles
FROM netflix_titles
WHERE country IS NOT NULL
  AND country <> 'Unknown'
GROUP BY country, type
ORDER BY total_titles DESC;

-- 19. Find movies longer than 120 minutes
-- Works when duration values are stored like '130 min'
SELECT title, duration, release_year
FROM netflix_titles
WHERE type = 'Movie'
  AND CAST(REPLACE(duration, ' min', '') AS INTEGER) > 120
ORDER BY CAST(REPLACE(duration, ' min', '') AS INTEGER) DESC;

-- 20. Find TV Shows with more than 3 seasons
-- Works when duration values are stored like '4 Seasons'
SELECT title, duration, release_year
FROM netflix_titles
WHERE type = 'TV Show'
  AND CAST(
        REPLACE(
            REPLACE(duration, ' Seasons', ''),
            ' Season',
            ''
        ) AS INTEGER
      ) > 3
ORDER BY CAST(
        REPLACE(
            REPLACE(duration, ' Seasons', ''),
            ' Season',
            ''
        ) AS INTEGER
      ) DESC;
