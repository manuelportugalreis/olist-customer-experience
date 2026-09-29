-- Which large product categories generate the most dissatisfaction, and is it logistics or product?
SELECT
    COALESCE(t.product_category_name_english, p.product_category_name, 'unknown') AS category,
    COUNT(DISTINCT d.order_id)                     AS orders,
    ROUND(AVG(d.review_score <= 2) * 100, 1)       AS pct_bad_reviews,
    ROUND(AVG(d.is_late) * 100, 1)                 AS pct_late,
    ROUND(AVG(CASE WHEN d.is_late = 0 THEN d.review_score <= 2 END) * 100, 1) AS pct_bad_when_on_time
FROM delivered_orders d
JOIN order_items i ON i.order_id = d.order_id
JOIN products p    ON p.product_id = i.product_id
LEFT JOIN category_translation t ON t.product_category_name = p.product_category_name
WHERE d.review_score IS NOT NULL
GROUP BY category
HAVING COUNT(DISTINCT d.order_id) >= 2000
ORDER BY pct_bad_reviews DESC;
