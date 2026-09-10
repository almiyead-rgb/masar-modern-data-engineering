{{ config(tags=['premerge']) }}
-- Source freshness alone would miss null or future arrival timestamps.
select trip_id from {{ ref('stg_trips') }}
where _ingested_at is null or _ingested_at > current_timestamp() + interval 5 minutes
   or _batch_id is null or _batch_id = ''
   or _source_sha256 is null or not _source_sha256 rlike '^[a-f0-9]{64}$'

union all
select driver_id from {{ source('bronze','drivers') }}
where _ingested_at is null or _ingested_at > current_timestamp() + interval 5 minutes
union all
select _batch_id from {{ source('bronze','gps_events') }}
where _ingested_at is null or _ingested_at > current_timestamp() + interval 5 minutes
