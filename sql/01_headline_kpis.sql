-- How big is the business, and how often do customers come back?
WITH per_customer AS (
    SELECT customer_unique_id, COUNT(*) AS n_orders
    FROM delivered_orders
    GROUP BY customer_unique_id
)
SELECT
    (SELECT COUNT(*) FROM delivered_orders)                          AS delivered_orders,
    COUNT(*)                                                         AS customers,
    ROUND(AVG(n_orders > 1) * 100, 1)                                AS pct_customers_who_repurchased,
    (SELECT ROUND(SUM(items_value) / 1e6, 2) FROM delivered_orders)  AS revenue_million_brl,
    (SELECT ROUND(AVG(is_late) * 100, 1) FROM delivered_orders)      AS pct_orders_late,
    (SELECT ROUND(AVG(review_score), 2) FROM delivered_orders)       AS avg_review_score
FROM per_customer;
