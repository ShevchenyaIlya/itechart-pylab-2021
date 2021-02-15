SELECT * FROM posts INNER JOIN users ON (posts.owner=users.user_id) INNER JOIN categories ON (posts.post_category=categories.category_id)
WHERE category_name=COALESCE(%s, category_name) AND post_date=COALESCE(%s, post_date) AND votes_number >= COALESCE(%s, votes_number) AND votes_number <= COALESCE(%s, votes_number)
ORDER BY %s %s
LIMIT %s OFFSET %s;