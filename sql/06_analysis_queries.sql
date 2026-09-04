-- 06_analysis_queries.sql
-- Analytical queries for E-Commerce database analysis.
-- Run these queries inside the 'ecommerce_olist' database.

-- 1. Total Revenue
SELECT
    ROUND(SUM(payment_value), 2) AS total_revenue
FROM payments;

-- 2. Total Orders
SELECT
    COUNT(*) AS total_orders
FROM orders;

-- 3. Average Order Value
SELECT
    ROUND(SUM(payment_value) / COUNT(DISTINCT order_id), 2) AS average_order_value
FROM payments;

-- 4. Revenue by Month
SELECT
    DATE_TRUNC('month', o.order_purchase_timestamp) AS month,
    ROUND(SUM(p.payment_value), 2) AS revenue
FROM orders o
JOIN payments p ON o.order_id = p.order_id
WHERE o.order_status <> 'canceled'
GROUP BY 1;

-- 5. Revenue by Product Category
SELECT
    COALESCE(t.product_category_name_english, p.product_category_name, 'unknown') AS category_english,
    ROUND(SUM(oi.price), 2) AS revenue
FROM orders o
JOIN order_items oi ON o.order_id = oi.order_id
JOIN products p ON oi.product_id = p.product_id
LEFT JOIN category_translation t ON p.product_category_name = t.product_category_name
WHERE o.order_status <> 'canceled'
GROUP BY 1
ORDER BY revenue DESC;

-- 6. Top 10 Products by Revenue
SELECT
    oi.product_id,
    SUM(oi.price) AS revenue
FROM order_items oi
GROUP BY oi.product_id
ORDER BY revenue DESC;

-- 7. Top 10 Sellers by Revenue
SELECT
    seller_id,
    ROUND(SUM(price), 2) AS revenue
FROM order_items
GROUP BY seller_id;

-- 8. Sales by State
SELECT
    c.customer_state,
    ROUND(SUM(oi.price), 2) AS revenue
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
JOIN order_items oi ON o.order_id = oi.order_id
WHERE o.order_status <> 'canceled'
GROUP BY c.customer_state
ORDER BY revenue DESC;

-- 9. Payment Method Analysis
SELECT
    payment_type,
    COUNT(*) AS transactions,
    ROUND(SUM(payment_value), 2) AS revenue
FROM payments
GROUP BY payment_type
ORDER BY revenue DESC;

-- 10. Delivery Performance
SELECT
    AVG(
        EXTRACT(
            DAY FROM
            (order_delivered_customer_date -
             order_purchase_timestamp)
        )
    ) AS avg_delivery_days
FROM orders
WHERE order_delivered_customer_date IS NOT NULL;

-- 11. Late Delivery Analysis
SELECT
    CASE 
        WHEN order_delivered_customer_date > order_estimated_delivery_date THEN 'Late'
        ELSE 'On Time'
    END AS delivery_status,
    COUNT(*) AS total_orders,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (), 2) AS pct_of_orders
FROM orders
WHERE order_delivered_customer_date IS NOT NULL
GROUP BY 1;

-- 12. Customer Lifetime Value
SELECT *
FROM vw_customer_lifetime_value
ORDER BY lifetime_value DESC;
