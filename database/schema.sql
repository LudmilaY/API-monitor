CREATE TABLE plants (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    location VARCHAR(255)
);

CREATE TABLE inverter (
    id SERIAL PRIMARY KEY,
    model VARCHAR(255),
    plant_id INTEGER REFERENCES plants(id) ON DELETE CASCADE
);

CREATE TABLE metrics (
    id SERIAL PRIMARY KEY,
    date_time TIMESTAMP WITH TIME ZONE NOT NULL,
    active_power_watt FLOAT,
    temperature_celsius FLOAT,
    inverter_id INTEGER REFERENCES inverter (id) ON DELETE CASCADE
);

CREATE INDEX idx_metrics_datetime ON metrics(date_time);
CREATE INDEX idx_metrics_inverter ON metrics(inverter_id);