-- Dynamic Manpower Allocation

-- Problem:* Given a table `manpower_allocation` with columns `person_id`, `shift_start`, `shift_end`, `state`, and `availability`, 
--  write a query to:
--     - Find the optimal allocation of manpower to orders in different states.
--     - Ensure availability is balanced across shifts, particularly during peak hours.
with work_force as (
SELECT person_id,state, datediff(shift_end,shift_start) as long_hours
FROM manpower_allocation_data
where availability !='Unavailable')
select * from work_force
where long_hours>0;
-- --------------------------------------------------------------------------
-- defined peak_hours
with peak_hours as (
    SELECT '01:00:00' AS start_time, '3:00:00' AS end_time
),
work_force as (
select person_id,
      shift_start,
      shift_end,
      state,
      availability,
      datediff(shift_end,shift_start) as Shift_duration_in_day,
      case
        when shift_start>=(select start_time from peak_hours) and
        shift_end<=(Select end_time from peak_hours) then 'peak_time'
        else 'off_peak' end as Work_load
from manpower_allocation_data
where availability !='Unavailable'
)
select state,work_load,count(person_id) as Worker_count,sum(Shift_duration_in_day) as duration
from  work_force
group by 1,2;



