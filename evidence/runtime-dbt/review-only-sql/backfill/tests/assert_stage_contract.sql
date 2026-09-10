-- JINJA-ONLY STRUCTURAL REVIEW. NOT dbt compile or Spark execution.

-- Singular test: any returned row is a failure. Never silently discard it.
select trip_id from masar_review.stg_trips
where trip_id is null or trip_id = '' or city is null
   or start_utc is null or end_utc is null or end_utc <= start_utc
   or fare_sar is null or fare_sar < 0
   or distance_km is null or distance_km <= 0
   or _source_file is null or _source_file not in ('trips.csv', 'late_trips.csv', 'correction.csv')
   or not trim(raw_start_ts) rlike '^[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}(Z|[+-](0[0-9]|1[0-4]):[0-5][0-9])$'
   or not trim(raw_end_ts) rlike '^[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}(Z|[+-](0[0-9]|1[0-4]):[0-5][0-9])$'