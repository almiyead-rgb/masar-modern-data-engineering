-- JINJA-ONLY STRUCTURAL REVIEW. NOT dbt compile or Spark execution.
-- Global totals must reconcile even though mart and fact have different grains.
with silver as (
 select count(*) as n, coalesce(sum(fare_sar),0) as fare from masar_review.silver_trips
), mart as (
 select coalesce(sum(trip_count),0) as n, coalesce(sum(total_fare_sar),0) as fare
 from masar_review.mart_city_daily
)
select silver.n from silver cross join mart
where silver.n != mart.n or silver.fare != mart.fare