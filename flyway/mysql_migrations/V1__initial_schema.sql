CREATE TABLE precipitation_details (
    id INT AUTO_INCREMENT PRIMARY KEY,
    condition_text VARCHAR(255) NOT NULL,
    precip_mm FLOAT NOT NULL,
    humidity INT NOT NULL,
    cloud INT NOT NULL,
    should_go_outside BOOLEAN NOT NULL
);

CREATE TABLE weather_data (
    id INT AUTO_INCREMENT PRIMARY KEY,
    country VARCHAR(100) NOT NULL,
    location_name VARCHAR(255) NOT NULL,
    last_updated DATETIME NOT NULL,
    temperature_celsius FLOAT NOT NULL,
    wind_kph FLOAT,
    wind_degree INT,
    wind_direction VARCHAR(50),
    feels_like_celsius FLOAT,
    visibility_km FLOAT,
    uv_index FLOAT,
    sunrise VARCHAR(20),
    sunset VARCHAR(20),

    precipitation_details_id INT NOT NULL,
    FOREIGN KEY (precipitation_details_id) REFERENCES precipitation_details(id)
);