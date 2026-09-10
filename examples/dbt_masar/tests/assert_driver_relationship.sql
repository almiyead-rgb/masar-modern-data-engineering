{{ config(tags=['premerge']) }}
select t.trip_id from {{ ref('stg_trips') }} t
left anti join {{ ref('stg_drivers') }} d on t.driver_id = d.driver_id
