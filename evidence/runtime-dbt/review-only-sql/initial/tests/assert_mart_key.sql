-- JINJA-ONLY STRUCTURAL REVIEW. NOT dbt compile or Spark execution.
select trip_date_local, city from masar_review.mart_city_daily
group by trip_date_local, city having count(*) != 1