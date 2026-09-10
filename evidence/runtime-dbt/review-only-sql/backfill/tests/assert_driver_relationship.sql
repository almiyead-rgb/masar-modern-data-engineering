-- JINJA-ONLY STRUCTURAL REVIEW. NOT dbt compile or Spark execution.

select t.trip_id from masar_review.stg_trips t
left anti join masar_review.stg_drivers d on t.driver_id = d.driver_id