CREATE TABLE users (
    user_id BIGINT PRIMARY KEY,
    username VARCHAR(100) UNIQUE,
    name VARCHAR(100),
    surname VARCHAR(100),
    age INT CHECK (age >= 12 AND age <= 999),
    phone_number VARCHAR(20),
    language VARCHAR(2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);