{{ config(tags=['premerge']) }}
select cast(driver_id as string) as bad_id from {{ ref('stg_drivers') }}
where driver_id is null or driver_id = '' or vehicle_type is null
   or vehicle_type not in ('sedan','suv')
   or driver_rating is null or driver_rating < 0 or driver_rating > 5
union all
select cast(event_id as string) from {{ ref('stg_gps') }}
where event_id is null or event_id = '' or event_utc is null
   or latitude is null or longitude is null or isnan(latitude) or isnan(longitude)
   or latitude not between -90 and 90 or longitude not between -180 and 180
   or synthetic is null or synthetic = false
union all
select cast(g.event_id as string) from {{ ref('stg_gps') }} g
left anti join {{ ref('stg_trips') }} t on g.trip_id = t.trip_id
