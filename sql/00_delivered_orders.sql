-- One row per delivered order with the facts used across the analysis.
-- Created as a view so every later query starts from the same definition.
DROP VIEW IF EXISTS delivered_orders;
CREATE VIEW delivered_orders AS
WITH reviews AS (
    SELECT order_id, AVG(review_score) AS review_score
    FROM order_reviews
    GROUP BY order_id
),
items AS (
    SELECT order_id,
           COUNT(*)                   AS n_items,
           COUNT(DISTINCT seller_id)  AS n_sellers,
           SUM(price)                 AS items_value,
           SUM(freight_value)         AS freight_value
    FROM order_items
    GROUP BY order_id
)
SELECT
    o.order_id,
    c.customer_unique_id,
    c.customer_state,
    o.order_purchase_timestamp,
    julianday(o.order_estimated_delivery_date) - julianday(o.order_purchase_timestamp) AS promised_days,
    julianday(o.order_delivered_customer_date) - julianday(o.order_purchase_timestamp) AS actual_days,
    julianday(o.order_delivered_customer_date) - julianday(o.order_estimated_delivery_date) AS days_late,
    o.order_delivered_customer_date > o.order_estimated_delivery_date AS is_late,
    i.n_items,
    i.n_sellers,
    i.items_value,
    i.freight_value,
    r.review_score
FROM orders o
JOIN customers c ON c.customer_id = o.customer_id
JOIN items i     ON i.order_id = o.order_id
LEFT JOIN reviews r ON r.order_id = o.order_id
WHERE o.order_status = 'delivered'
  AND o.order_delivered_customer_date IS NOT NULL;
