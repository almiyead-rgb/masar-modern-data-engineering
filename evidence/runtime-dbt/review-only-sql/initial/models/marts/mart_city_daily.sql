-- JINJA-ONLY STRUCTURAL REVIEW. NOT dbt compile or Spark execution.
-- Small learner-facing aggregate built from Silver, not receipt-grain staging.
select trip_date_local, city, count(*) as trip_count,
       cast(sum(fare_sar) as decimal(16,2)) as total_fare_sar
from masar_review.silver_trips
group by trip_date_local, city