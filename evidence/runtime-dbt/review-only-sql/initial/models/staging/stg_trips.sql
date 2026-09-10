-- JINJA-ONLY STRUCTURAL REVIEW. NOT dbt compile or Spark execution.
-- Receipt-grain staging. Execution is pending; source files remain unchanged.
with typed as (
    select
        trim(trip_id) as trip_id,
        trim(driver_id) as driver_id,
        case lower(trim(city))
          when 'riyadh' then 'Riyadh'
          when 'jeddah' then 'Jeddah'
          when 'dammam' then 'Dammam'
        end as city,
        try_cast(trim(start_ts) as timestamp) as start_utc,
        try_cast(trim(end_ts) as timestamp) as end_utc,
        case when trim(fare_sar) rlike '^[+-]?[0-9]+([.][0-9]{1,2})?$'
             then try_cast(trim(fare_sar) as decimal(12,2)) end as fare_sar,
        case when trim(distance_km) rlike '^[+-]?[0-9]+([.][0-9]{1,2})?$'
             then try_cast(trim(distance_km) as decimal(12,2)) end as distance_km,
        case when _source_file = 'correction.csv' then 2 else 1 end as source_revision,
        _source_file, _source_sha256, _batch_id, _ingested_at,
        start_ts as raw_start_ts, end_ts as raw_end_ts
    from bronze_review.trips
)
select *,
    unix_timestamp(end_utc) - unix_timestamp(start_utc) as duration_seconds,
    to_date(from_utc_timestamp(start_utc, 'Asia/Riyadh')) as trip_date_local
from typed