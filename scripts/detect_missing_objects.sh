#!/bin/bash
duckdb -c "
WITH counts AS (
    SELECT object_id, COUNT(DISTINCT regexp_extract(filename, 'providers/([^/]+)/', 1)) as p_count
    FROM read_csv_auto('../providers/*/observations.csv', filename=true)
    GROUP BY object_id
)
SELECT object_id || ' missing in some providers'
FROM counts WHERE p_count < 3;" --no-header
