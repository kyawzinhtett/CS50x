SELECT AVG(ratings.rating) AS avg_rating
FROM ratings
JOIN movies ON movies.id = ratings.movie_id
WHERE movies.year = 2012;