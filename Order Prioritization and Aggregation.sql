-- **Order Prioritization and Aggregation**

-- - **Problem:** Given an orders table with `order_id`, `user_id`, `order_date`, `state`, and `order_value`, write a query to:
--     - Identify the states with the highest order values.
--     - Aggregate order values by state and calculate a moving average for each state to identify trends over time.
use interview_prep;
with cte as (
select state,sum(order_value) as total_value
from order_prioritization_data
group by state
), ranking as
(
select state,total_value,rank()over(order by state desc) as total_ranking
from cte
group by state
)
select * from ranking;

with total_sell as (
select state,sum(order_value) as total_value
from order_prioritization_data
group by state
), moving_avg as
(
select state,
total_value,
avg(total_value)over(order by total_value rows between 2 preceding and current row) as rolling_avg
from total_Sell
)
select state,
       total_value,
       round(rolling_avg,2) as Moving_average 
from moving_avg;
