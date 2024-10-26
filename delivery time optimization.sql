create database interview_prep;
-- 1. **Distance Calculation for Delivery Optimization**
--     - **Problem:** Given a table of customer orders with columns like `customer_id`, `latitude`, `longitude`, `state`, `delivery_person_id`, 
--          and `order_time`, write a query to:
--         - Assign delivery personnel to each customer order based on proximity.
--         - Calculate the distance between delivery personnel and customers (e.g., using the Haversine formula).
--         - Prioritize unassigned orders for closer personnel and minimize delivery time.
-- ---------------------------------------------------------------------------------------------------
with distance_params as  (
select distinct c_d.customer_id as customer_id,
c_d.latitude as customer_lat,
c_d.longitude as customer_lon,
c_d.state as customer_state,
-- ---------------------------------
d_d.delivery_person_id as delivery_person,
d_d.latitude as delivery_lat,
d_d.longitude as delivery_lon,
d_d.delivery_area as delivery_area,
--  ------------------------------------
-- Euclidean calc for proximity
sqrt(power(c_d.latitude - d_d.latitude,2)+power(c_d.longitude-d_d.longitude,2)) as distance
from delivery_optimization_data as c_d
join geo_data as d_d on c_d.delivery_person_id=d_d.delivery_person_id and 
c_d.order_time<d_d.delivery_time and c_d.customer_id<>d_d.delivery_person_id
)
-- Assingn the closet person to each order
select 
      dp.customer_id,
      dp.customer_state,
      dp.delivery_person as Assinged_delivery_person,
      dp.delivery_area as Comming_from,
      dp.distance as Far_from_location
from distance_params as dp
join (
select customer_id,min(distance) as min_distance from distance_params group by customer_id
) as find_close
on dp.customer_id=find_close.customer_id and dp.distance=find_close.min_distance
order by 1;

--  Calculate the distance between delivery personnel and customers (e.g., using the Haversine formula).
with cte as (
select 
distinct customer_id,
g_d.delivery_person_id,
6371 * 2 * ASIN(SQRT(POWER(SIN((RADIANS(d_o.latitude) - RADIANS(g_d.latitude)) / 2), 2) +
COS(RADIANS(g_d.latitude)) * COS(RADIANS(d_o.latitude)) * 
POWER(SIN((RADIANS(d_o.longitude) - RADIANS(g_d.longitude)) / 2), 2))) as distance
 from delivery_optimization_data as d_o
join geo_data as g_d on d_o.delivery_person_id=g_d.delivery_person_id and 
d_o.customer_id<>g_d.delivery_person_id and d_o.order_time<g_d.delivery_time
)
select customer_id,delivery_person_id,min(distance) as distance from cte
group by 1,2
order by 1;
-- ----------------------------------------------------------------------------
-- Prioritize unassigned orders for closer personnel and minimize delivery time.
WITH DistanceCalc AS (
    SELECT 
        d_o.customer_id,
        d_o.state,
        d_o.delivery_person_id,  -- This will be NULL for unassigned orders
        o_p.order_id,
        o_p.order_value,
        g_d.delivery_person_id AS available_delivery_person_id,  -- Delivery personnel ID
        6371 * 2 * ASIN(SQRT(POWER(SIN((RADIANS(d_o.latitude) - RADIANS(g_d.latitude)) / 2), 2) +
        COS(RADIANS(g_d.latitude)) * COS(RADIANS(d_o.latitude)) * 
        POWER(SIN((RADIANS(d_o.longitude) - RADIANS(g_d.longitude)) / 2), 2))) AS distance
    FROM 
        delivery_optimization_data AS d_o
    JOIN 
        order_prioritization_data AS o_p ON d_o.state = o_p.state 
        AND d_o.order_time < o_p.order_date 
        AND o_p.user_id <> d_o.customer_id
    JOIN 
        geo_data AS g_d ON d_o.delivery_person_id = g_d.delivery_person_id
    WHERE 
        d_o.delivery_person_id IS NULL  -- Focus on unassigned orders
)

SELECT 
    customer_id,
    order_id,
    order_value,
    available_delivery_person_id,
    distance
FROM 
    DistanceCalc
WHERE 
    (customer_id, distance) IN (
        SELECT 
            customer_id, MIN(distance) 
        FROM 
            DistanceCalc 
        GROUP BY 
            customer_id
    );

