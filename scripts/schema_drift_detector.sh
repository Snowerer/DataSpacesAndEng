#!/bin/bash
duckdb -c "
WITH schema_counts AS (
    SELECT 'satellite_A' as p, COUNT(*) as c FROM (DESCRIBE SELECT * FROM '../providers/satellite_A/observations.csv')
    UNION ALL
    SELECT 'satellite_B' as p, COUNT(*) as c FROM (DESCRIBE SELECT * FROM '../providers/satellite_B/observations.csv')
    UNION ALL
    SELECT 'ground_station' as p, COUNT(*) as c FROM (DESCRIBE SELECT * FROM '../providers/ground_station/observations.csv')
)
SELECT 
    CASE WHEN COUNT(DISTINCT c) = 1 THEN 'SCHEMA STATUS: CONSISTENT'
    ELSE 'SCHEMA DRIFT DETECTED' END
FROM schema_counts;" -noheader
