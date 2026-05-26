#!/bin/bash
duckdb -c "
SELECT 
    a.object_id, 
    'Inconsistency detected (temp diff > 0.5):',
    'A: ' || a.temperature, 
    'B: ' || b.temperature
FROM '../providers/satellite_A/observations.csv' a
JOIN '../providers/satellite_B/observations.csv' b ON a.object_id = b.object_id AND a.timestamp = b.timestamp
WHERE abs(a.temperature - b.temperature) > 0.5;" --no-header
