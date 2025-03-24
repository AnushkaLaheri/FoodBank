-- DROP TABLE users
CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
	username varchar(255) not null
);

-- DROP TABLE foods
CREATE TABLE foods (
    food_id SERIAL PRIMARY KEY,
    food_name VARCHAR(255) NOT NULL,
	expiry TIMESTAMP NOT NULL
);

-- DROP TABLE points
CREATE TABLE points (
    point_id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(user_id),
    food_id INT REFERENCES foods(food_id),
    time_submitted TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    points_awarded INT NOT NULL
);

INSERT INTO users (username) VALUES
('John Doe'),
('Jane Doe');

INSERT INTO foods (food_name, expiry) VALUES
('Canned Beans', '2024-12-29'),
('Rice', '2025-06-30'),
('Canned Tuna', '2024-11-29');

INSERT INTO points (user_id, food_id, time_submitted, points_awarded) VALUES
(1, 1, '2024-09-28 14:30:00', 10);

INSERT INTO points (user_id, food_id, time_submitted, points_awarded) VALUES
(2, 2, '2024-09-28 15:00:00', 20);

INSERT INTO points (user_id, food_id, time_submitted, points_awarded) VALUES
(1, 3, '2024-09-28 15:30:00', 30);