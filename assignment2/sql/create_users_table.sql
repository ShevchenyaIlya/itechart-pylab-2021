CREATE TABLE IF NOT EXISTS users(
    user_id BIGSERIAL PRIMARY KEY NOT NULL,
    username VARCHAR(50) UNIQUE,
    user_karma BIGINT NOT NULL,
    user_cake_day DATE NOT NULL,
    post_karma BIGINT NOT NULL,
    comment_karma BIGINT NOT NULL);