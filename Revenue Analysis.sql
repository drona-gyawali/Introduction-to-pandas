-- Revenue and Retention Analysis

-- - Problem: In an e-commerce setting, use a dataset with `user_id`, `order_id`, `order_date`, and `order_amount` to:
--     - Calculate customer retention by comparing order dates.
--     - Determine customer segments based on spending habits and repeat orders.

-- ---------------- Retention Rate Calcultion-----------------------------------------------------
WITH previous_cus AS (
    SELECT DISTINCT user_id
    FROM order_prioritization_data
    WHERE order_date >= DATE_SUB(CURDATE(), INTERVAL 2 MONTH) -- Start of the previous month
      AND order_date < DATE_SUB(CURDATE(), INTERVAL 1 MONTH)  -- End of the previous month
),
current_cus AS (  
    SELECT DISTINCT user_id
    FROM order_prioritization_data
    WHERE order_date >= DATE_SUB(CURDATE(), INTERVAL 1 MONTH) -- Start of the current month
      AND order_date < CURDATE()                               -- End of the current month
),
retained_cus AS (
    SELECT pc.user_id
    FROM previous_cus pc
    JOIN current_cus cc ON pc.user_id = cc.user_id
)
SELECT 
    COUNT(rc.user_id) * 1.0 / COUNT(pc.user_id) AS retention_rate
FROM 
    previous_cus pc
LEFT JOIN 
    retained_cus rc ON pc.user_id = rc.user_id;
    
-- -------------------Customer Spend Habits and Purchase POWER-----------------------------------------
with spend as (
select user_id,
       round(sum(order_value),2) as Total_spent,
       count(order_id) as Total_purchases
 from order_prioritization_data
 group by 1
)
select user_id,Total_spent,Total_purchases
from spend
order by Total_spent desc;


select * from order_prioritization_data