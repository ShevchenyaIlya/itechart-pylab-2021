INSERT INTO posts(unique_id, post_url, post_date, comments_number, votes_number, post_category, owner)
VALUES(%s, %s, %s, %s, %s, %s, (SELECT user_id from users WHERE username=%s));