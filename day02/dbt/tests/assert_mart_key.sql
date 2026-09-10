select trip_date_local, city from {{ ref('mart_city_daily') }}
group by trip_date_local, city having count(*) != 1
