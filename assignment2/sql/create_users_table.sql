CREATE TABLE IF NOT EXISTS users(
    user_id BIGSERIAL PRIMARY KEY NOT NULL,
    username VARCHAR(50) UNIQUE,
    user_karma VARCHAR(10) NOT NULL,
    user_cake_day DATE NOT NULL,
    post_karma VARCHAR(10) NOT NULL,
    comment_karma VARCHAR(10) NOT NULL);