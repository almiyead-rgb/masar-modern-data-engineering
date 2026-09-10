-- JINJA-ONLY STRUCTURAL REVIEW. NOT dbt compile or Spark execution.
-- One current row per trip. Look back on ingestion time, not trip event date.
-- A late June trip must not disappear because the session is run in September.
with candidates as (
    select * from masar_review.int_trip_candidates
    
    where _ingested_at >= (
      select coalesce(max(_ingested_at), cast('1970-01-01 00:00:00' as timestamp))
             - interval 3 days from masar_review.silver_trips
    )
    
)
select s.* from candidates s

left join masar_review.silver_trips t on s.trip_id = t.trip_id
where t.trip_id is null or s.source_revision > t.source_revision
