-- 04_indexes.sql
-- Performance optimization indexes for E-Commerce analytics queries.
-- Run this script inside the 'ecommerce_olist' database.

DROP INDEX IF EXISTS idx_orders_customer;
DROP INDEX IF EXISTS idx_orders_purchase_date;
DROP INDEX IF EXISTS idx_order_items_product;
DROP INDEX IF EXISTS idx_order_items_seller;
DROP INDEX IF EXISTS idx_payments_order;
DROP INDEX IF EXISTS idx_reviews_order;

CREATE INDEX idx_orders_customer
ON orders(customer_id);

CREATE INDEX idx_orders_purchase_date
ON orders(order_purchase_timestamp);

CREATE INDEX idx_order_items_product
ON order_items(product_id);

CREATE INDEX idx_order_items_seller
ON order_items(seller_id);

CREATE INDEX idx_payments_order
ON payments(order_id);

CREATE INDEX idx_reviews_order
ON reviews(order_id);

ANALYZE;
