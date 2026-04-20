#!/bin/bash
duckdb -c "
WITH object_counts AS (
    SELECT object_id, COUNT(DISTINCT regexp_extract(filename, 'providers/([^/]+)/', 1)) as p_count
    FROM read_csv_auto('../providers/*/observations.csv', filename=true)
    GROUP BY object_id
),
stats AS (
    SELECT 
        COUNT(*) as total_objs,
        SUM(CASE WHEN p_count = 3 THEN 1 ELSE 0 END) as full_cov
    FROM object_counts
)
SELECT 
    'TOTAL OBJECTS: ' || total_objs,
    'FULL COVERAGE: ' || full_cov,
    'COVERAGE SCORE: ' || round(full_cov * 100.0 / total_objs, 1) || '%'
FROM stats;" -noheader
