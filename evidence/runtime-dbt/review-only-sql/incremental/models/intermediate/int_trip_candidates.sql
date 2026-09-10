-- JINJA-ONLY STRUCTURAL REVIEW. NOT dbt compile or Spark execution.
-- Rank the full receipt history BEFORE the incremental ingestion-time filter.
-- Pre-merge tests reject same-revision conflicts; this ranking never hides them.
with enriched as (
    select t.*, d.vehicle_type, d.driver_rating,
        sha2(to_json(named_struct(
          'driver_id', t.driver_id, 'city', t.city,
          'start_utc', t.start_utc, 'end_utc', t.end_utc,
          'fare_sar', t.fare_sar, 'distance_km', t.distance_km,
          'vehicle_type', d.vehicle_type, 'driver_rating', d.driver_rating)), 256) as _payload_hash
    from masar_review.stg_trips t
    left join masar_review.stg_drivers d using (driver_id)
), ranked as (
    select *, row_number() over (
      partition by trip_id order by source_revision desc, _ingested_at desc,
      _source_sha256 asc, _batch_id asc) as receipt_rank
    from enriched
)
select trip_id, driver_id, city, start_utc, end_utc, trip_date_local,
       fare_sar, distance_km, duration_seconds, vehicle_type, driver_rating,
       source_revision, _source_file, _source_sha256, _ingested_at, _payload_hash
from ranked where receipt_rank = 1