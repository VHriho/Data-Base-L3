CREATE TABLE precipitation_details (
    id SERIAL PRIMARY KEY,
    condition_text VARCHAR(255) NOT NULL,
    precip_mm FLOAT NOT NULL,
    humidity INTEGER NOT NULL,
    cloud INTEGER NOT NULL,
    should_go_outside BOOLEAN,
    UNIQUE (condition_text, precip_mm, humidity, cloud, should_go_outside)
);

CREATE TABLE weather_data (
    id SERIAL PRIMARY KEY,
    country VARCHAR(100) NOT NULL,
    location_name VARCHAR(255) NOT NULL,
    last_updated TIMESTAMP WITHOUT TIME ZONE NOT NULL,
    temperature_celsius FLOAT NOT NULL,
    wind_kph FLOAT NOT NULL,
    wind_degree INTEGER NOT NULL,
    wind_direction VARCHAR(10) NOT NULL,
    feels_like_celsius FLOAT NOT NULL,
    visibility_km FLOAT NOT NULL,
    uv_index FLOAT NOT NULL,
    sunrise VARCHAR(10) NOT NULL,
    sunset VARCHAR(10) NOT NULL,

    precipitation_details_id INTEGER NOT NULL,
    CONSTRAINT fk_precipitation_details
        FOREIGN KEY (precipitation_details_id)
        REFERENCES precipitation_details (id)
        ON DELETE RESTRICT
);