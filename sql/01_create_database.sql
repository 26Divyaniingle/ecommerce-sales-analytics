-- 01_create_database.sql
-- Create the ecommerce_sales database.
-- Note: Run this script with superuser privileges (e.g., as 'postgres' user).

-- Drop database if exists (uncomment if you want a fresh start)
DROP DATABASE IF EXISTS ecommerce_olist;

CREATE DATABASE ecommerce_olist
    WITH 
    OWNER = postgres
    ENCODING = 'UTF8'
    CONNECTION LIMIT = -1;

COMMENT ON DATABASE ecommerce_olist IS 'Database containing Olist e-commerce analytics data';
