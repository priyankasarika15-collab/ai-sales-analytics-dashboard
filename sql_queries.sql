-- Run these queries against the SQLite table named sales.
-- Revenue and profit are already calculated per order line in the sample dataset.

-- 1. Overall KPIs
SELECT
    ROUND(SUM(revenue), 2) AS total_revenue,
    ROUND(SUM(profit), 2) AS total_profit,
    COUNT(DISTINCT order_id) AS total_orders,
    SUM(quantity) AS units_sold,
    ROUND(100.0 * SUM(profit) / NULLIF(SUM(revenue), 0), 2) AS profit_margin_pct
FROM sales;

-- 2. Monthly revenue and profit
SELECT strftime('%Y-%m', order_date) AS month,
       ROUND(SUM(revenue), 2) AS revenue,
       ROUND(SUM(profit), 2) AS profit
FROM sales
GROUP BY month
ORDER BY month;

-- 3. Best-performing products
SELECT product, category,
       SUM(quantity) AS units_sold,
       ROUND(SUM(revenue), 2) AS revenue,
       ROUND(SUM(profit), 2) AS profit
FROM sales
GROUP BY product, category
ORDER BY revenue DESC;

-- 4. Regional performance
SELECT region,
       COUNT(DISTINCT order_id) AS orders,
       ROUND(SUM(revenue), 2) AS revenue,
       ROUND(SUM(profit), 2) AS profit
FROM sales
GROUP BY region
ORDER BY revenue DESC;

-- 5. Sales channel mix
SELECT sales_channel,
       COUNT(DISTINCT order_id) AS orders,
       ROUND(SUM(revenue), 2) AS revenue
FROM sales
GROUP BY sales_channel
ORDER BY revenue DESC;

-- 6. Products with negative total profit (if any)
SELECT product, ROUND(SUM(profit), 2) AS total_profit
FROM sales
GROUP BY product
HAVING SUM(profit) < 0
ORDER BY total_profit;

-- 7. Average order value
SELECT ROUND(SUM(revenue) / NULLIF(COUNT(DISTINCT order_id), 0), 2) AS average_order_value
FROM sales;
