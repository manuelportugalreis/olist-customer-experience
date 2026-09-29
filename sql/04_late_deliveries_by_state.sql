-- Where are late deliveries concentrated? (states with at least 500 orders)
SELECT
    customer_state,
    COUNT(*)                              AS orders,
    ROUND(AVG(promised_days), 1)          AS avg_promised_days,
    ROUND(AVG(actual_days), 1)            AS avg_actual_days,
    ROUND(AVG(is_late) * 100, 1)          AS pct_late,
    ROUND(AVG(review_score), 2)           AS avg_review_score
FROM delivered_orders
GROUP BY customer_state
HAVING COUNT(*) >= 500
ORDER BY pct_late DESC;
