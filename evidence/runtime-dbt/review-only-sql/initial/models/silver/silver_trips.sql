-- JINJA-ONLY STRUCTURAL REVIEW. NOT dbt compile or Spark execution.
-- One current row per trip. Look back on ingestion time, not trip event date.
-- A late June trip must not disappear because the session is run in September.
with candidates as (
    select * from masar_review.int_trip_candidates
    
)
select s.* from candidates s
