-- ========================================================
-- PRE-VALIDATED ANALYTICAL QUERIES FOR SQL AGENT
-- Read-Only, Safe Aggregations & Trend Analysis
-- ========================================================

-- 1. Top 10 Products by Total Revenue
SELECT 
    p.product_name,
    p.category,
    SUM(s.quantity) AS total_units_sold,
    SUM(s.revenue) AS total_revenue,
    SUM(s.profit) AS total_profit
FROM sales s
JOIN products p ON s.product_id = p.product_id
GROUP BY p.product_id, p.product_name, p.category
ORDER BY total_revenue DESC
LIMIT 10;

-- 2. Monthly Revenue Comparison for Hyderabad Branch
SELECT 
    strftime('%Y-%m', sale_date) AS sales_month,
    city,
    COUNT(DISTINCT order_id) AS total_orders,
    SUM(revenue) AS monthly_revenue,
    SUM(profit) AS monthly_profit
FROM sales
WHERE city = 'Hyderabad'
GROUP BY strftime('%Y-%m', sale_date), city
ORDER BY sales_month ASC;

-- 3. Hyderabad Sales Decline Breakdown by Product (August vs September 2026)
SELECT 
    p.product_name,
    SUM(CASE WHEN strftime('%Y-%m', s.sale_date) = '2026-08' THEN s.revenue ELSE 0 END) AS august_revenue,
    SUM(CASE WHEN strftime('%Y-%m', s.sale_date) = '2026-09' THEN s.revenue ELSE 0 END) AS september_revenue,
    SUM(CASE WHEN strftime('%Y-%m', s.sale_date) = '2026-09' THEN s.revenue ELSE 0 END) - 
    SUM(CASE WHEN strftime('%Y-%m', s.sale_date) = '2026-08' THEN s.revenue ELSE 0 END) AS absolute_change
FROM sales s
JOIN products p ON s.product_id = p.product_id
WHERE s.city = 'Hyderabad' 
  AND strftime('%Y-%m', s.sale_date) IN ('2026-08', '2026-09')
GROUP BY p.product_id, p.product_name
ORDER BY absolute_change ASC;

-- 4. High-Risk Churn Customers with Pending Support Tickets
SELECT 
    customer_id,
    customer_name,
    city,
    segment,
    days_since_last_order,
    support_tickets_count,
    churn_risk_score,
    total_spend
FROM customers
WHERE churn_risk_score >= 0.70
ORDER BY churn_risk_score DESC, total_spend DESC
LIMIT 15;

-- 5. Inventory Depletion & Reorder Status (SOP Trigger)
SELECT 
    product_id,
    product_name,
    category,
    stock_quantity,
    CASE 
        WHEN stock_quantity < 20 THEN 'CRITICAL - REORDER IMMEDIATELY'
        WHEN stock_quantity < 50 THEN 'LOW - MONITOR BUFFER'
        ELSE 'HEALTHY'
    END AS stock_status
FROM products
WHERE stock_quantity < 50
ORDER BY stock_quantity ASC;
