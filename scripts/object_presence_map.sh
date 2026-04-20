#!/bin/bash
echo "OBJECT | A | B | G"
echo "-------------------"
duckdb -c "
SELECT 
    object_id as OBJECT,
    MAX(CASE WHEN filename LIKE '%satellite_A%' THEN 'X' ELSE '-' END) as A,
    MAX(CASE WHEN filename LIKE '%satellite_B%' THEN 'X' ELSE '-' END) as B,
    MAX(CASE WHEN filename LIKE '%ground_station%' THEN 'X' ELSE '-' END) as G
FROM read_csv_auto('../providers/*/observations.csv', filename=true)
GROUP BY object_id
ORDER BY object_id;" --no-header
