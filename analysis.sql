-- =========================================================
-- DELIVERY SLA BREACH ANALYSIS
-- SQL Analysis Queries
-- =========================================================


-- =========================================================
-- QUERY 1: SLA BREACH RATE BY STORE
-- Purpose:
-- Identify stores with the highest percentage of
-- SLA-breached orders.
-- =========================================================

SELECT 
    store_id,
    COUNT(*) AS total_orders,
    ROUND(
        AVG(
            CASE 
                WHEN breached = 1 THEN 1.0 
                ELSE 0 
            END
        ) * 100,
        1
    ) AS breach_rate_pct
FROM orders
GROUP BY store_id
ORDER BY breach_rate_pct DESC;


-- =========================================================
-- QUERY 2: SLA BREACH RATE BY HOUR
-- Purpose:
-- Identify which hours of the day have the highest
-- SLA breach rates.
-- =========================================================

SELECT 
    hour_of_day,
    ROUND(
        AVG(
            CASE 
                WHEN breached = 1 THEN 1.0 
                ELSE 0 
            END
        ) * 100,
        1
    ) AS breach_rate_pct,
    COUNT(*) AS orders
FROM orders
GROUP BY hour_of_day
ORDER BY breach_rate_pct DESC;


-- =========================================================
-- QUERY 3: SLA BREACH RATE BY DAY OF WEEK
-- Purpose:
-- Compare SLA breach rates across different days
-- of the week.
-- =========================================================

SELECT 
    day_of_week,
    ROUND(
        AVG(
            CASE 
                WHEN breached = 1 THEN 1.0 
                ELSE 0 
            END
        ) * 100,
        1
    ) AS breach_rate_pct
FROM orders
GROUP BY day_of_week
ORDER BY breach_rate_pct DESC;


-- =========================================================
-- QUERY 4: 7-DAY ROLLING SLA BREACH RATE BY STORE
-- Purpose:
-- Track recent SLA performance for each store using
-- a 7-day rolling breach rate.
--
-- Demonstrates:
-- CTEs
-- Window functions
-- PARTITION BY
-- ORDER BY
-- ROWS BETWEEN
-- =========================================================

WITH daily_store AS (
    SELECT
        store_id,
        DATE(order_placed_time) AS order_date,
        AVG(
            CASE 
                WHEN breached = 1 THEN 1.0 
                ELSE 0 
            END
        ) AS daily_breach_rate
    FROM orders
    GROUP BY 
        store_id,
        DATE(order_placed_time)
)

SELECT
    store_id,
    order_date,
    ROUND(
        AVG(daily_breach_rate) OVER (
            PARTITION BY store_id
            ORDER BY order_date
            ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
        ) * 100,
        1
    ) AS rolling_7day_breach_rate_pct
FROM daily_store
ORDER BY 
    store_id,
    order_date;