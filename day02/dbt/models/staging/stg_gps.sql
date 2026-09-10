-- A parsed model is not a Kafka or streaming implementation.
with parsed as (
    select from_json(raw_json,
        'event_id string, trip_id string, city string, event_ts string, synthetic boolean, location struct<lat:double,lon:double>') as e,
        _batch_id
    from {{ source('bronze', 'gps_events') }}
)
select e.event_id as event_id, e.trip_id as trip_id,
       try_cast(e.event_ts as timestamp) as event_utc,
       e.location.lat as latitude, e.location.lon as longitude,
       e.synthetic as synthetic, _batch_id
from parsed
