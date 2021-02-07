SELECT * FROM posts INNER JOIN users ON (posts.owner=users.user_id)
ORDER BY %s %s
LIMIT %s OFFSET %s;