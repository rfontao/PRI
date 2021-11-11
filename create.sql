DROP TABLE IF EXISTS show;
CREATE TABLE show (
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT NOT NULL,
    date_added TEXT NOT NULL,
    release_year INTEGER NOT NULL,
    duration INTEGER NOT NULL,
    --TODO
    rating TEXT, -- CHECK(rating IN (...))
    type TEXT CHECK(type IN ('M', 'S'))
);


DROP TABLE IF EXISTS country;
CREATE TABLE country (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL
);

DROP TABLE IF EXISTS country_show;
CREATE TABLE country_show (
    country_id INTEGER REFERENCES country(id),
    show_id INTEGER REFERENCES show(id),
    PRIMARY KEY (country_id, show_id)
);

DROP TABLE IF EXISTS genre;
CREATE TABLE genre (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL
);

DROP TABLE IF EXISTS genre_show;
CREATE TABLE genre_show (
    genre_id INTEGER REFERENCES genre(id),
    show_id INTEGER REFERENCES show(id),
    PRIMARY KEY (genre_id, show_id)
);

DROP TABLE IF EXISTS person;
CREATE TABLE person (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL
);

DROP TABLE IF EXISTS actor_show;
CREATE TABLE actor_show (
    actor_id INTEGER REFERENCES person(id),
    show_id INTEGER REFERENCES show(id),
    PRIMARY KEY (actor_id, show_id)
);

DROP TABLE IF EXISTS director_show;
CREATE TABLE director_show (
    director_id INTEGER REFERENCES person(id),
    show_id INTEGER REFERENCES show(id),
    PRIMARY KEY (director_id, show_id)
);

DROP TABLE IF EXISTS reviewer;
CREATE TABLE reviewer (
    id INTEGER PRIMARY KEY,
    name TEXT
);

DROP TABLE IF EXISTS review;
CREATE TABLE review (
    id INTEGER PRIMARY KEY,
    show_id INTEGER REFERENCES show(id),
    rating INTEGER,
    title TEXT,
    body TEXT,
    helpful_votes INTEGER,
    total_votes INTEGER,
    review_date TEXT,
    spoiler INTEGER CHECK (spoiler = 0 OR spoiler = 1),
    reviewer INTEGER REFERENCES reviewer(id)
);

