SELECT *
FROM posts
INNER JOIN users
    ON (posts.owner=users.user_id)
INNER JOIN categories
    ON (posts.post_category=categories.category_id);