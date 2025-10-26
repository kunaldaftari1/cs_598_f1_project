create table sessions (
    session_key INTEGER PRIMARY KEY,
    session_type TEXT NOT NULL,
    circuit_key INTEGER NOT NULL REFERENCES circuits(circuit_key),
    session_name TEXT NOT NULL,
    session_type TEXT NOT NULL,
    date_start DATE NOT NULL,
    date_end DATE NOT NULL,
    year INTEGER NOT NULL
);

create table starting_grid (
    session_key INTEGER NOT NULL REFERENCES sessions(session_key),
    driver_number INTEGER NOT NULL REFERENCES drivers(driver_number),
    position INTEGER NOT NULL,
    lap_duration FLOAT NOT NULL,

    PRIMARY KEY (session_key, driver_number)
);

create table race_result (
    session_key INTEGER NOT NULL REFERENCES sessions(session_key),
    driver_number INTEGER NOT NULL REFERENCES drivers(driver_number),
    position INTEGER NOT NULL,
    driver_status TEXT NOT NULL CHECK (driver_status IN ("dnf", "dns", "dsq", "finished")),

    PRIMARY KEY (session_key, driver_number)
)

create table circuits (
    circuit_key INTEGER PRIMARY KEY,
    country_name TEXT NOT NULL,
    country_code TEXT NOT NULL
);

create table drivers (
    driver_number INTEGER PRIMARY KEY,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    team_name TEXT NOT NULL REFERENCES teams(team_name)
    session_key INTEGER NOT NULL REFERENCES sessions(session_key)
);

create table teams (
    team_name TEXT PRIMARY KEY
);

create table laps (
    session_key INTEGER NOT NULL REFERENCES sessions(session_key),
    driver_number INTEGER NOT NULL REFERENCES drivers(driver_number),
    lap_number INTEGER NOT NULL,
    lap_duration FLOAT NOT NULL,
    i1_speed INTEGER,
    i2_speed INTEGER,
    st_speed INTEGER,
    is_pit_out_lap BOOLEAN

    PRIMARY KEY (session_key, driver_number, lap_number)
);

create table race_stints (
    session_key INTEGER NOT NULL REFERENCES sessions(session_key),
    driver_number INTEGER NOT NULL REFERENCES drivers(driver_number),
    lap_start INTEGER NOT NULL,
    lap_end INTEGER NOT NULL,
    compound TEXT NOT NULL CHECK (compound IN ("SOFT", "MEDIUM", "HARD")),
    tyre_life INTEGER NOT NULL

    PRIMARY KEY (session_key, driver_number)
);

create table overtakes (
    circuit_key INTEGER NOT NULL REFERENCES circuits(circuit_key),
    driver_number INTEGER NOT NULL REFERENCES drivers(driver_number),
    overtake_avg FLOAT

    PRIMARY KEY (driver_number, circuit_key)
);

create table weather (
    session_key INTEGER NOT NULL REFERENCES sessions(session_key),
    circuit_key INTEGER NOT NULL REFERENCES circuits(circuit_key),

    temperature FLOAT,
    humidity FLOAT,
    rainfall BOOLEAN,
    track_temperature FLOAT,
    wind_speed FLOAT,
    wind_direction FLOAT

    PRIMARY KEY (session_key, circuit_key)
);

create table pirelli_tyres (
    circuit_key INTEGER NOT NULL REFERENCES circuits(circuit_key),
    tyre_compound TEXT NOT NULL CHECK (tyre_compound IN ('C1', 'C2', 'C3', 'C4', 'C5', 'C6')),
    year INTEGER NOT NULL,

    PRIMARY KEY (circuit_key, year)
);