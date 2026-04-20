#!/bin/bash
duckdb -c "
WITH totals AS (SELECT COUNT(*) as grand_total FROM '../providers/*/observations.csv')
SELECT 
    regexp_extract(filename, 'providers/([^/]+)/', 1) || ': ' || 
    COUNT(*) || ' (' || round(COUNT(*) * 100.0 / (SELECT grand_total FROM totals), 1) || '%)'
FROM read_csv_auto('../providers/*/observations.csv', filename=true)
GROUP BY filename
ORDER BY COUNT(*) DESC;" -noheader
