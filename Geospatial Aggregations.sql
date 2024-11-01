-- **Geospatial Aggregations**

-- - **Problem:** With a dataset of delivery locations (`latitude`, `longitude`, `delivery_area`, `delivery_person_id`), write a query to:
--     - Aggregate deliveries by delivery area.
--     - Identify which delivery areas experience the most delays based on delivery times, then optimize allocations accordingly.


select delivery_area,count(delivery_person_id) as Delivery_personnel
 from geo_data
group by delivery_area
order by Delivery_personnel desc;

select delivery_area,delivery_time,
case when delivery_time>Date_ADD(delivery_time,interval -30 minute) then 'delayed' else 'Genral' end as TIme_labeled
 from geo_data
 order by delivery_time desc
