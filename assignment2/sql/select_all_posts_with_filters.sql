SELECT * FROM posts INNER JOIN users ON (posts.owner=users.user_id)
%s
%s
LIMIT %s OFFSET %s;