CREATE TABLE IF NOT EXISTS posts(
    post_id BIGSERIAL PRIMARY KEY NOT NULL,
    unique_id uuid UNIQUE NOT NULL,
    post_url TEXT,
    post_date DATE NOT NULL,
    comments_number VARCHAR(10) NOT NULL,
    votes_number VARCHAR(10) NOT NULL,
    post_category VARCHAR(20) NOT NULL,
    owner SMALLSERIAL REFERENCES users(user_id));