-- One current row per trip. Look back on ingestion time, not trip event date.
-- A late June trip must not disappear because the session is run in September.
with candidates as (
    select * from {{ ref('int_trip_candidates') }}
    {% if is_incremental() and not var('reprocess_all', false) %}
    where _ingested_at >= (
      select coalesce(max(_ingested_at), cast('1970-01-01 00:00:00' as timestamp))
             - interval 3 days from {{ this }}
    )
    {% endif %}
)
select s.* from candidates s
{% if is_incremental() %}
left join {{ this }} t on s.trip_id = t.trip_id
where t.trip_id is null or s.source_revision > t.source_revision
{% endif %}
