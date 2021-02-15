SELECT * FROM posts INNER JOIN users ON (posts.owner=users.user_id)
WHERE post_category=COALESCE(%s, post_category) AND
      post_date=COALESCE(%s, post_date) AND (
        votes_number >= COALESCE(%s, votes_number) AND
        votes_number <= COALESCE(%s, votes_number)
     )
ORDER BY %s %s
LIMIT %s OFFSET %s;