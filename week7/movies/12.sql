SELECT movies.title
FROM movies
JOIN stars j ON j.movie_id = movies.id
JOIN stars h ON h.movie_id = movies.id
JOIN people jd ON jd.id = j.person_id
JOIN people hc ON hc.id = h.person_id
WHERE jd.name = 'Johnny Depp' AND
    hc.name = 'Helena Bonham Carter';