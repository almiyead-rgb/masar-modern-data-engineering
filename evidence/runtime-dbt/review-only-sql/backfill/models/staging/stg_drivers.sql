-- JINJA-ONLY STRUCTURAL REVIEW. NOT dbt compile or Spark execution.
-- Authored design. UTC session and isolated source registration are prerequisites.
select trim(driver_id) as driver_id,
       lower(trim(vehicle_type)) as vehicle_type,
       case when trim(driver_rating) rlike '^[0-9]([.][0-9])?$'
            then try_cast(driver_rating as decimal(3,1)) end as driver_rating
from bronze_review.drivers