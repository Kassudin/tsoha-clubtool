CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    player_name TEXT UNIQUE,
    password TEXT,
    player_number INTEGER UNIQUE,
    position TEXT,
    coach BOOLEAN DEFAULT FALSE
);

CREATE TABLE events (
    id SERIAL PRIMARY KEY,
    event_type TEXT,
    event_date DATE NOT NULL,
    event_start_time TIME NOT NULL,
    event_end_time TIME NOT NULL,
    event_location TEXT NOT NULL,
    event_description TEXT
);