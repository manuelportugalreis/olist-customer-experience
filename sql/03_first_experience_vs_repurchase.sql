-- Do customers whose first order went badly come back less?
-- Only first orders placed before March 2018, so every customer had at least ~7 months to return.
WITH ranked AS (
    SELECT *,
           ROW_NUMBER() OVER (PARTITION BY customer_unique_id ORDER BY order_purchase_timestamp) AS order_rank,
           COUNT(*)     OVER (PARTITION BY customer_unique_id)                                  AS n_orders
    FROM delivered_orders
)
SELECT
    CASE WHEN is_late = 1 THEN 'late' ELSE 'on time' END AS first_delivery,
    CASE
        WHEN review_score <= 2 THEN '1. bad (1-2)'
        WHEN review_score < 4  THEN '2. neutral (3)'
        ELSE                        '3. good (4-5)'
    END                                          AS first_review,
    COUNT(*)                                     AS customers,
    ROUND(AVG(n_orders > 1) * 100, 2)            AS pct_repurchased
FROM ranked
WHERE order_rank = 1
  AND order_purchase_timestamp < '2018-03-01'
  AND review_score IS NOT NULL
GROUP BY first_delivery, first_review
ORDER BY first_delivery, first_review;
