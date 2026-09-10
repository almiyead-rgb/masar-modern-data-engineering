-- Read-only query over the pinned native fact view in Lab 08.
-- One row per city proxy; never join raw GPS events into a money aggregation.
SELECT zone_key,
       COUNT(*) AS trip_count,
       CAST(SUM(fare_sar) AS DECIMAL(20,2)) AS total_fare_sar,
       SUM(duration_seconds) AS total_duration_seconds,
       CAST(SUM(duration_seconds) AS DOUBLE) / COUNT(*) AS average_duration_seconds
FROM masar_day05_fact
GROUP BY zone_key
ORDER BY zone_key;
