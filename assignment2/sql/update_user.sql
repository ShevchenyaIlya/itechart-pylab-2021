UPDATE users
SET
    user_karma = %s,
    user_cake_day = %s,
    post_karma = %s,
    comment_karma = %s
WHERE username=%s;