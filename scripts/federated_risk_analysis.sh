#!/bin/bash
duckdb -c "
WITH totals AS (
    SELECT 
        (SELECT COUNT(*) FROM '../providers/*/observations.csv') as full_count,
        (SELECT COUNT(*) FROM read_csv_auto(['../providers/satellite_A/observations.csv','../providers/satellite_B/observations.csv'])) as fed_count
)
SELECT 
    'FULL: ' || full_count,
    'FEDERATED: ' || fed_count,
    'MISSING: ' || (full_count - fed_count),
    'LOSS: ' || round((full_count - fed_count) * 100.0 / full_count, 1) || '%'
FROM totals;" --no-header
