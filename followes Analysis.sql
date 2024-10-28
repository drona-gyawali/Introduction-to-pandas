-- Follower and Influencer Analysis

-- - Problem: For a social media dataset with tables `users` and `follows` (where `follows` has columns `follower_id`, `followee_id`),
--     write a query to:
--     - Calculate the top influencers based on followers' engagement.
--     - Rank users by the number of unique followers and interactions within the last 30 days.
use interview_prep;

with follower as ( 
select followee_id as user_id ,count(  distinct follower_id) as Total_fans
 from follows_data
 group by 1
 order by 2 desc,1 asc
)
select * from follower;

select followee_id  as users, count( distinct follower_id) as followers
from follows_data
WHERE interaction_date >= CURDATE() - INTERVAL 30 DAY
group by 1
order by 2 desc;

select * from follows_data;