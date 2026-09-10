-- JINJA-ONLY STRUCTURAL REVIEW. NOT dbt compile or Spark execution.

-- Content conflicts are not ordinary duplicate receipts.
select trip_id, source_revision
from masar_review.stg_trips
group by trip_id, source_revision
having count(distinct to_json(named_struct(
    'driver_id',driver_id,'city',city,'start',start_utc,'end',end_utc,
    'fare',fare_sar,'distance',distance_km))) > 1