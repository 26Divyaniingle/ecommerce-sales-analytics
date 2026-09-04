-- 03_load_data.sql
-- Direct CSV data import using PostgreSQL COPY or \copy command.
-- Ensure you run this inside the 'ecommerce_olist' database.

-- IMPORTANT NOTE on Path:
-- Modify the path placeholders below to point to the absolute path of your cleaned CSV files.

-- ============================================================================
-- METHOD 1: Using psql client '\copy' command (RECOMMENDED - runs as local user)
-- Execute these lines in your psql terminal:
-- ============================================================================
/*
\copy customers FROM 'path/to/data/processed/customers_cleaned.csv' DELIMITER ',' CSV HEADER;
\copy sellers FROM 'path/to/data/processed/sellers_cleaned.csv' DELIMITER ',' CSV HEADER;
\copy products FROM 'path/to/data/processed/products_cleaned.csv' DELIMITER ',' CSV HEADER;
\copy category_translation FROM 'path/to/data/processed/category_translation_cleaned.csv' DELIMITER ',' CSV HEADER;
\copy geolocation FROM 'path/to/data/processed/geolocation_cleaned.csv' DELIMITER ',' CSV HEADER;
\copy orders FROM 'path/to/data/processed/orders_cleaned.csv' DELIMITER ',' CSV HEADER;
\copy order_items FROM 'path/to/data/processed/order_items_cleaned.csv' DELIMITER ',' CSV HEADER;
\copy payments FROM 'path/to/data/processed/payments_cleaned.csv' DELIMITER ',' CSV HEADER;
\copy reviews FROM 'path/to/data/processed/reviews_cleaned.csv' DELIMITER ',' CSV HEADER;
*/


-- ============================================================================
-- METHOD 2: Using Server-side SQL 'COPY' (Requires database superuser privileges)
-- ============================================================================
-- Un-comment the blocks below and replace '/absolute/path/to/...' with actual paths.

/*
BEGIN;

COPY customers 
FROM '/absolute/path/to/data/processed/customers_cleaned.csv' 
DELIMITER ',' CSV HEADER;

COPY sellers 
FROM '/absolute/path/to/data/processed/sellers_cleaned.csv' 
DELIMITER ',' CSV HEADER;

COPY products 
FROM '/absolute/path/to/data/processed/products_cleaned.csv' 
DELIMITER ',' CSV HEADER;

COPY category_translation 
FROM '/absolute/path/to/data/processed/category_translation_cleaned.csv' 
DELIMITER ',' CSV HEADER;

COPY geolocation 
FROM '/absolute/path/to/data/processed/geolocation_cleaned.csv' 
DELIMITER ',' CSV HEADER;

COPY orders 
FROM '/absolute/path/to/data/processed/orders_cleaned.csv' 
DELIMITER ',' CSV HEADER;

COPY order_items 
FROM '/absolute/path/to/data/processed/order_items_cleaned.csv' 
DELIMITER ',' CSV HEADER;

COPY payments 
FROM '/absolute/path/to/data/processed/payments_cleaned.csv' 
DELIMITER ',' CSV HEADER;

COPY reviews 
FROM '/absolute/path/to/data/processed/reviews_cleaned.csv' 
DELIMITER ',' CSV HEADER;

COMMIT;
*/
