CREATE TABLE IF NOT EXISTS users(
    user_id BIGSERIAL PRIMARY KEY NOT NULL,
    username VARCHAR(50) UNIQUE,
    user_karma BIGINT NOT NULL,
    user_cake_day DATE NOT NULL,
    post_karma BIGINT NOT NULL,
    comment_karma BIGINT NOT NULL);

CREATE TABLE IF NOT EXISTS posts(
    post_id BIGSERIAL PRIMARY KEY NOT NULL,
    unique_id uuid UNIQUE NOT NULL,
    post_url TEXT,
    post_date DATE NOT NULL,
    comments_number BIGINT NOT NULL,
    votes_number BIGINT NOT NULL,
    post_category VARCHAR(20) NOT NULL,
    owner BIGSERIAL REFERENCES users(user_id));