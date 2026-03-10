CREATE TABLE IF NOT EXISTS properties (
    id SERIAL PRIMARY KEY,
    city VARCHAR(80) NOT NULL,
    district VARCHAR(80) NOT NULL,
    area_m2 NUMERIC NOT NULL,
    rooms INT NOT NULL,
    year_built INT NOT NULL,
    energy_rating CHAR(1) NOT NULL,
    listing_price_eur NUMERIC NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS analyses (
    id SERIAL PRIMARY KEY,
    property_id INT REFERENCES properties(id),
    fair_price_eur NUMERIC,
    market_gap_pct NUMERIC,
    anomaly_label VARCHAR(40),
    risk_explanation TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);

-- TODO (Person 2): add migration strategy (Alembic) instead of raw SQL-only evolution.
