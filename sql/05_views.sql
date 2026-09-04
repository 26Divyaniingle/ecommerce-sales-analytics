-- 05_views.sql
-- Analytical Views for reporting and BI tools (Power BI).
-- Run this script inside the 'ecommerce_olist' database.

DROP VIEW IF EXISTS vw_product_performance;
DROP VIEW IF EXISTS vw_seller_performance;
DROP VIEW IF EXISTS vw_customer_lifetime_value;
DROP VIEW IF EXISTS vw_delivery_performance;
DROP VIEW IF EXISTS vw_payment_analysis;
DROP VIEW IF EXISTS vw_state_sales;
DROP VIEW IF EXISTS vw_category_sales;
DROP VIEW IF EXISTS vw_monthly_sales;

-- 1. Monthly Sales View
CREATE VIEW vw_monthly_sales AS
SELECT
    DATE_TRUNC('month', o.order_purchase_timestamp)::DATE AS month,
    COUNT(DISTINCT o.order_id) AS total_orders,
    SUM(p.payment_value) AS total_revenue
FROM orders o
JOIN payments p ON o.order_id = p.order_id
WHERE o.order_status <> 'canceled'
GROUP BY 1;

-- 2. Category Sales View
CREATE VIEW vw_category_sales AS
SELECT
    COALESCE(t.product_category_name_english, p.product_category_name, 'unknown') AS category_english,
    p.product_category_name AS category_portuguese,
    COUNT(DISTINCT oi.order_id) AS total_orders,
    SUM(oi.price) AS total_sales_revenue
FROM order_items oi
JOIN products p ON oi.product_id = p.product_id
LEFT JOIN category_translation t ON p.product_category_name = t.product_category_name
GROUP BY 1, 2;

-- 3. State Sales View
CREATE VIEW vw_state_sales AS
SELECT
    c.customer_state,
    COUNT(DISTINCT c.customer_unique_id) AS total_unique_customers,
    COUNT(DISTINCT o.order_id) AS total_orders,
    SUM(oi.price) AS total_spending
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
JOIN order_items oi ON o.order_id = oi.order_id
WHERE o.order_status <> 'canceled'
GROUP BY c.customer_state;

-- 4. Payment Analysis View
CREATE VIEW vw_payment_analysis AS
SELECT
    payment_type,
    COUNT(*) AS transactions,
    ROUND(SUM(payment_value), 2) AS revenue
FROM payments
GROUP BY payment_type;

-- 5. Delivery Performance View
CREATE VIEW vw_delivery_performance AS
SELECT
    order_id,
    order_status,
    order_purchase_timestamp,
    order_delivered_customer_date,
    order_estimated_delivery_date,
    EXTRACT(DAY FROM (order_delivered_customer_date - order_purchase_timestamp)) AS actual_delivery_days,
    CASE
        WHEN order_delivered_customer_date > order_estimated_delivery_date THEN 'Late'
        WHEN order_delivered_customer_date IS NULL THEN 'Not Delivered'
        ELSE 'On Time'
    END AS delivery_status
FROM orders;

-- 6. Customer Lifetime Value View
CREATE VIEW vw_customer_lifetime_value AS
SELECT
    c.customer_unique_id,
    c.customer_city,
    c.customer_state,
    COUNT(DISTINCT o.order_id) AS total_orders,
    ROUND(SUM(p.payment_value), 2) AS lifetime_value
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
JOIN payments p ON o.order_id = p.order_id
WHERE o.order_status <> 'canceled'
GROUP BY
    c.customer_unique_id,
    c.customer_city,
    c.customer_state;

-- 7. Seller Performance View
CREATE VIEW vw_seller_performance AS
SELECT
    s.seller_id,
    s.seller_city,
    s.seller_state,
    COUNT(DISTINCT oi.order_id) AS orders_handled,
    SUM(oi.price) AS total_sales,
    ROUND(AVG(oi.price), 2) AS average_item_price
FROM sellers s
JOIN order_items oi ON s.seller_id = oi.seller_id
JOIN orders o ON oi.order_id = o.order_id
WHERE o.order_status <> 'canceled'
GROUP BY s.seller_id, s.seller_city, s.seller_state;

-- 8. Product Performance View
CREATE VIEW vw_product_performance AS
SELECT
    oi.product_id,
    p.product_category_name,
    COUNT(DISTINCT oi.order_id) AS orders_count,
    SUM(oi.price) AS revenue
FROM order_items oi
JOIN products p ON oi.product_id = p.product_id
GROUP BY oi.product_id, p.product_category_name;
