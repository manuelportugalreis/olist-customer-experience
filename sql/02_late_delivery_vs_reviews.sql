-- Does a late delivery change how customers rate the purchase?
SELECT
    CASE
        WHEN days_late <= -7 THEN '1. 7+ days early'
        WHEN days_late <= 0  THEN '2. 0-7 days early'
        WHEN days_late <= 7  THEN '3. 1-7 days late'
        ELSE                      '4. 7+ days late'
    END                                        AS delivery_bucket,
    COUNT(*)                                   AS orders,
    ROUND(AVG(review_score), 2)                AS avg_review_score,
    ROUND(AVG(review_score <= 2) * 100, 1)     AS pct_bad_reviews
FROM delivered_orders
WHERE review_score IS NOT NULL
GROUP BY delivery_bucket
ORDER BY delivery_bucket;
