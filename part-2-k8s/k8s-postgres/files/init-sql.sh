#!/bin/bash

# Step 1: Create the database if it doesn't exist
DB_EXISTS=$(psql -h {{ .Values.init.database.host }} -U {{ .Values.init.database.user }} -tAc "SELECT 1 FROM pg_database WHERE datname='{{ .Values.init.database.name }}'")
if [ "$DB_EXISTS" != "1" ]; then
  echo "Creating database {{ .Values.init.database.name }}..."
  psql -h {{ .Values.init.database.host }} -U {{ .Values.init.database.user }} -d postgres -c "CREATE DATABASE {{ .Values.init.database.name }};"
else
  echo "Database {{ .Values.init.database.name }} already exists."
fi

# Step 2: Create tables and indexes in {{ .Values.init.database.name }}
psql -h {{ .Values.init.database.host }} -U {{ .Values.init.database.user }} -v ON_ERROR_STOP=1 -d {{ .Values.init.database.name }} <<EOF
-- Dimension Tables

CREATE TYPE STATUS_CORE_ENUM AS ENUM (
  'active',
  'inactive',
  'unknown',
  'expended',
  'lost',
  'retired'
);

CREATE TYPE STATUS_LAUNCH_SITE_ENUM AS ENUM (
  'active',
  'inactive',
  'unknown',
  'retired',
  'lost',
  'under construction'
);

CREATE TYPE CREW_STATUS_ENUM AS ENUM (
  'active',
  'inactive',
  'retired',
  'unknown'
);

CREATE TYPE CAPSULES_STATUS_ENUM AS ENUM (
  'unknown',
  'active',
  'retired',
  'destroyed'
);

CREATE TYPE CAPSULES_TYPE_ENUM AS ENUM (
  'Dragon 1.0',
  'Dragon 1.1',
  'Dragon 2.0'
);

CREATE TYPE LANDPAD_STATUS_ENUM AS ENUM (
  'active',
  'inactive',
  'unknown',
  'retired',
  'lost',
  'under construction'
);

CREATE TYPE DATE_PRECISION_LAUNCHES_ENUM AS ENUM (
  'half',
  'quarter',
  'year',
  'month',
  'day',
  'hour'
);

-- Core Dimension
CREATE TABLE IF NOT EXISTS dim_core (
    id SERIAL PRIMARY KEY,
    external_core_id VARCHAR(24) CHECK (external_core_id ~ '^[0-9a-f]{24}$') UNIQUE NOT NULL,
    serial VARCHAR(50) NOT NULL,
    block INTEGER,
    status STATUS_CORE_ENUM NOT NULL,
    reuse_count INTEGER DEFAULT 0,
    rtls_attempts INTEGER  DEFAULT 0,
    rtls_landings INTEGER DEFAULT 0,
    asds_attempts INTEGER DEFAULT 0,
    asds_landings INTEGER DEFAULT 0,
    last_update TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Launch Site Dimension
CREATE TABLE IF NOT EXISTS dim_launch_site (
    id SERIAL PRIMARY KEY,
    external_site_id VARCHAR(24) CHECK (external_site_id ~ '^[0-9a-f]{24}$') UNIQUE NOT NULL,
    name VARCHAR(100),
    full_name VARCHAR(200),
    status STATUS_LAUNCH_SITE_ENUM NOT NULL,
    locality VARCHAR(100),
    region VARCHAR(100),
    timezone VARCHAR(100),
    latitude DECIMAL(10, 8),
    longitude DECIMAL(11, 8),
    launch_attempts INTEGER DEFAULT 0,
    launch_successes INTEGER  DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Failure Dimension
CREATE TABLE IF NOT EXISTS dim_failure (
    id SERIAL PRIMARY KEY,
    time INTEGER,
    altitude INTEGER,
    reason TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Fairings Dimension
CREATE TABLE IF NOT EXISTS dim_fairings (
    id SERIAL PRIMARY KEY,
    reused BOOLEAN,
    recovery_attempt BOOLEAN,
    recovered BOOLEAN,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Rocket Dimension
CREATE TABLE IF NOT EXISTS dim_rocket (
    id SERIAL PRIMARY KEY,
    external_rocket_id VARCHAR(24) CHECK (external_rocket_id ~ '^[0-9a-f]{24}$') UNIQUE NOT NULL,
    name VARCHAR(100),
    type VARCHAR(50),
    active BOOLEAN,
    stages INTEGER,
    boosters INTEGER,
    cost_per_launch INTEGER,
    success_rate_pct INTEGER,
    first_flight DATE,
    country VARCHAR(100),
    company VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Payload Dimension
CREATE TABLE IF NOT EXISTS dim_payload (
    id SERIAL PRIMARY KEY,
    external_payload_id VARCHAR(24) CHECK (external_payload_id ~ '^[0-9a-f]{24}$') UNIQUE NOT NULL,
    name VARCHAR(100) UNIQUE,
    type VARCHAR(50),
    mass_kg DECIMAL(10, 2),
    mass_lbs DECIMAL(10, 2),
    orbit VARCHAR(50),
    reference_system VARCHAR(50),
    regime VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Crew Dimension
CREATE TABLE IF NOT EXISTS dim_crew (
    id SERIAL PRIMARY KEY,
    external_crew_id VARCHAR(24) CHECK (external_crew_id ~ '^[0-9a-f]{24}$') UNIQUE NOT NULL,
    name VARCHAR(100),
    status CREW_STATUS_ENUM NOT NULL,
    agency VARCHAR(100),
    image TEXT,
    wikipedia TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Ship Dimension
CREATE TABLE IF NOT EXISTS dim_ship (
    id SERIAL PRIMARY KEY,
    external_ship_id VARCHAR(24) CHECK (external_ship_id ~ '^[0-9a-f]{24}$') UNIQUE NOT NULL,
    name VARCHAR(100) UNIQUE NOT NULL,
    type VARCHAR(50),
    active BOOLEAN,
    imo VARCHAR(50),
    mmsi VARCHAR(50),
    abs VARCHAR(50),
    class VARCHAR(50),
    mass_kg DECIMAL(10, 2),
    mass_lbs DECIMAL(10, 2),
    year_built INTEGER,
    home_port VARCHAR(100),
    status VARCHAR(50),
    speed_kn DECIMAL(10, 2),
    course_deg DECIMAL(10, 2),
    latitude DECIMAL(10, 8),
    longitude DECIMAL(11, 8),
    last_ais_update TIMESTAMP,
    link TEXT,
    image TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Capsule Dimension
CREATE TABLE IF NOT EXISTS dim_capsule (
    id SERIAL PRIMARY KEY,
    external_capsule_id VARCHAR(24) CHECK (external_capsule_id ~ '^[0-9a-f]{24}$') UNIQUE NOT NULL,
    serial VARCHAR(50) UNIQUE NOT NULL,
    status CAPSULES_STATUS_ENUM NOT NULL,
    type CAPSULES_TYPE_ENUM NOT NULL,
    water_landings INTEGER DEFAULT 0,
    land_landings INTEGER DEFAULT 0,
    last_update TEXT,
    reuse_count INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Landpad Dimension
CREATE TABLE IF NOT EXISTS dim_landpad (
    id SERIAL PRIMARY KEY,
    external_landpad_id VARCHAR(24) CHECK (external_landpad_id ~ '^[0-9a-f]{24}$') UNIQUE NOT NULL,
    name VARCHAR(100),
    full_name VARCHAR(200),
    status LANDPAD_STATUS_ENUM NOT NULL,
    type VARCHAR(50),
    locality VARCHAR(100),
    region VARCHAR(100),
    latitude DECIMAL(10, 8),
    longitude DECIMAL(11, 8),
    landing_attempts INTEGER,
    landing_successes INTEGER,
    wikipedia TEXT,
    details TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Starlink Dimension
CREATE TABLE IF NOT EXISTS dim_starlink (
    id SERIAL PRIMARY KEY,
    external_starlink_id VARCHAR(24) CHECK (external_starlink_id ~ '^[0-9a-f]{24}$') UNIQUE NOT NULL,
    version VARCHAR(50),
    launch VARCHAR(50),
    longitude DECIMAL(11, 8),
    latitude DECIMAL(10, 8),
    height_km DECIMAL(10, 2),
    velocity_kms DECIMAL(10, 2),
    -- spaceTrack JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Roadster Dimension
CREATE TABLE IF NOT EXISTS dim_roadster (
    id SERIAL PRIMARY KEY,
    external_roadster_id VARCHAR(24) CHECK (external_roadster_id ~ '^[0-9a-f]{24}$') UNIQUE NOT NULL,
    name VARCHAR(100),
    launch_date_utc TIMESTAMP,
    launch_date_unix BIGINT,
    launch_mass_kg DECIMAL(20, 9),
    launch_mass_lbs DECIMAL(20, 9),
    norad_id INTEGER,
    epoch_jd DECIMAL(20, 9),
    orbit_type VARCHAR(50),
    apoapsis_au DECIMAL(20, 9),
    periapsis_au DECIMAL(20, 9),
    semi_major_axis_au DECIMAL(20, 9),
    eccentricity DECIMAL(20, 9),
    inclination DECIMAL(20, 9),
    longitude DECIMAL(20, 9),
    periapsis_arg DECIMAL(20, 9),
    period_days DECIMAL(20, 9),
    speed_kph DECIMAL(20, 9),
    speed_mph DECIMAL(20, 9),
    earth_distance_km DECIMAL(20, 9),
    earth_distance_mi DECIMAL(20, 9),
    mars_distance_km DECIMAL(20, 9),
    mars_distance_mi DECIMAL(20, 9),
    flickr_images TEXT[],
    wikipedia TEXT,
    video TEXT,
    details TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Company Dimension
CREATE TABLE IF NOT EXISTS dim_company (
    id SERIAL PRIMARY KEY,
    external_company_id VARCHAR(24) CHECK (external_company_id ~ '^[0-9a-f]{24}$') UNIQUE NOT NULL,
    name VARCHAR(100),
    founder VARCHAR(100),
    founded INTEGER,
    employees INTEGER,
    vehicles INTEGER,
    launch_sites INTEGER,
    test_sites INTEGER,
    ceo VARCHAR(100),
    cto VARCHAR(100),
    coo VARCHAR(100),
    cto_propulsion VARCHAR(100),
    valuation BIGINT,
    -- headquarters JSONB,
    -- links JSONB,
    summary TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Fact Table (without core information)
CREATE TABLE IF NOT EXISTS fact_launches (
    id SERIAL PRIMARY KEY,
    external_launch_id VARCHAR(24) CHECK (external_launch_id ~ '^[0-9a-f]{24}$') UNIQUE NOT NULL,
    site_id INTEGER NOT NULL,
    rocket_id INTEGER NOT NULL,
    flight_number INTEGER NOT NULL,
    name VARCHAR(100) UNIQUE NOT NULL,
    details TEXT,
    date_utc TIMESTAMP NOT NULL,
    date_unix BIGINT NOT NULL,
    date_local TIMESTAMP NOT NULL,
    date_precision DATE_PRECISION_LAUNCHES_ENUM NOT NULL,
    success BOOLEAN,
    net BOOLEAN DEFAULT FALSE,
    launch_window INTEGER,
    upcoming BOOLEAN NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (rocket_id) REFERENCES dim_rocket(id),
    FOREIGN KEY (site_id) REFERENCES dim_launch_site(id)
);

-- Bridge table for launch-cores relationships
CREATE TABLE IF NOT EXISTS bridge_launch_core (
    launch_id INTEGER REFERENCES fact_launches(id),
    core_id INTEGER REFERENCES dim_core(id),
    flight INTEGER,
    gridfins BOOLEAN,
    legs BOOLEAN,
    reused BOOLEAN,
    landing_attempt BOOLEAN,
    landing_success BOOLEAN,
    landing_type TEXT,
    landpad_id INTEGER REFERENCES dim_landpad(id),
    PRIMARY KEY (launch_id, core_id)
);

-- Bridge table for launch-failures relationships
CREATE TABLE IF NOT EXISTS bridge_launch_failure (
    launch_id INTEGER REFERENCES fact_launches(id),
    failure_id INTEGER REFERENCES dim_failure(id),
    PRIMARY KEY (launch_id, failure_id)
);

-- Bridge table for launch-payloads relationships
CREATE TABLE IF NOT EXISTS bridge_launch_payload (
    launch_id INTEGER REFERENCES fact_launches(id),
    payload_id INTEGER REFERENCES dim_payload(id),
    PRIMARY KEY (launch_id, payload_id)
);

-- Bridge table for launch-crew relationships
CREATE TABLE IF NOT EXISTS bridge_launch_crew (
    launch_id INTEGER REFERENCES fact_launches(id),
    crew_id INTEGER REFERENCES dim_crew(id),
    PRIMARY KEY (launch_id, crew_id)
);

-- Bridge table for launch-ships relationships
CREATE TABLE IF NOT EXISTS bridge_launch_ship (
    launch_id INTEGER REFERENCES fact_launches(id),
    ship_id INTEGER REFERENCES dim_ship(id),
    PRIMARY KEY (launch_id, ship_id)
);

-- Bridge table for launch-capsules relationships
CREATE TABLE IF NOT EXISTS bridge_launch_capsule (
    launch_id INTEGER REFERENCES fact_launches(id),
    capsule_id INTEGER REFERENCES dim_capsule(id),
    PRIMARY KEY (launch_id, capsule_id)
);

-- Bridge table for launch-starlink relationships
CREATE TABLE IF NOT EXISTS bridge_launch_starlink (
    launch_id INTEGER REFERENCES fact_launches(id),
    starlink_id INTEGER REFERENCES dim_starlink(id),
    PRIMARY KEY (launch_id, starlink_id)
);

-- Create indexes
CREATE INDEX IF NOT EXISTS idx_launches_site ON fact_launches(site_id);
CREATE INDEX IF NOT EXISTS idx_launches_date ON fact_launches(date_utc);
CREATE INDEX IF NOT EXISTS idx_launch_cores_core ON bridge_launch_core(core_id);
CREATE INDEX IF NOT EXISTS idx_launch_payloads_payload ON bridge_launch_payload(payload_id);
CREATE INDEX IF NOT EXISTS idx_launch_crew_crew ON bridge_launch_crew(crew_id);
CREATE INDEX IF NOT EXISTS idx_launch_ships_ship ON bridge_launch_ship(ship_id);
CREATE INDEX IF NOT EXISTS idx_launch_capsules_capsule ON bridge_launch_capsule(capsule_id);

-- Create indexes for external IDs for efficient lookups
CREATE INDEX IF NOT EXISTS idx_core_external_id ON dim_core(external_core_id);
CREATE INDEX IF NOT EXISTS idx_launch_site_external_id ON dim_launch_site(external_site_id);
CREATE INDEX IF NOT EXISTS idx_rocket_external_id ON dim_rocket(external_rocket_id);
CREATE INDEX IF NOT EXISTS idx_payload_external_id ON dim_payload(external_payload_id);
CREATE INDEX IF NOT EXISTS idx_crew_external_id ON dim_crew(external_crew_id);
CREATE INDEX IF NOT EXISTS idx_ship_external_id ON dim_ship(external_ship_id);
CREATE INDEX IF NOT EXISTS idx_capsule_external_id ON dim_capsule(external_capsule_id);
CREATE INDEX IF NOT EXISTS idx_landpad_external_id ON dim_landpad(external_landpad_id);
CREATE INDEX IF NOT EXISTS idx_starlink_external_id ON dim_starlink(external_starlink_id);
CREATE INDEX IF NOT EXISTS idx_roadster_external_id ON dim_roadster(external_roadster_id);
CREATE INDEX IF NOT EXISTS idx_company_external_id ON dim_company(external_company_id);
CREATE INDEX IF NOT EXISTS idx_launch_external_id ON fact_launches(external_launch_id);
EOF 