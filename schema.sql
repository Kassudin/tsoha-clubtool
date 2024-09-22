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
CREATE TABLE event_registrations (
    user_id INTEGER REFERENCES users(id),
    event_id INTEGER REFERENCES events(id),
    status TEXT,
    UNIQUE (event_id, user_id)
);
INSERT INTO users (player_name, password, coach) VALUES ('Valkku', 'scrypt:32768:8:1$SAsGarfZzJqWEniE$de5ae17c0683a98ffdb26527a7d666b98225c701860893b9c8b38a4b01a8a3a2915053cc3ac677c084a68d976b27222b256c696659daeb0bd3cc46b07432ac87', TRUE); 
