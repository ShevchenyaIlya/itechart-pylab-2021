UPDATE posts
SET
  post_date = %s,
  post_url = %s,
  comments_number = %s,
  votes_number = %s,
  post_category = (SELECT category_id from categories WHERE category_name=%s),
  owner = (SELECT user_id from users WHERE username=%s)
WHERE unique_id=%s;