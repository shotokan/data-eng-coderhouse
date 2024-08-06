-- Verificar si la tabla existe y eliminarla si es así
DROP TABLE IF EXISTS isabido86_coderhouse.weather_data;

-- Crear la tabla con el campo ID autogenerado y ingest_timestamp para llevar el control
CREATE TABLE isabido86_coderhouse.weather_data (
    id INTEGER IDENTITY(1,1) PRIMARY KEY,
    name VARCHAR(255),
    region VARCHAR(255),
    country VARCHAR(255),
    lat FLOAT,
    lon FLOAT,
    tz_id VARCHAR(255),
    localtime_epoch BIGINT,
    local_time TIMESTAMP,
    ingest_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    current_last_updated_epoch BIGINT,
    current_last_updated TIMESTAMP,
    current_temp_c FLOAT,
    current_temp_f FLOAT,
    current_is_day INTEGER,
    current_condition_text VARCHAR(255),
    current_condition_icon VARCHAR(255),
    current_condition_code INTEGER,
    current_humidity INTEGER,
    current_cloud INTEGER,
    current_feelslike_c FLOAT,
    current_feelslike_f FLOAT,
    current_wind_mph FLOAT,
    current_wind_kph FLOAT,
    current_wind_degree INTEGER,
    current_wind_dir VARCHAR(10)
);