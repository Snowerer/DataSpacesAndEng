#!/bin/bash
duckdb -c "
SELECT 
    CASE WHEN 
        (SELECT COUNT(*) FROM '../providers/*/observations.csv') = 
        (SELECT COUNT(*) FROM read_csv_auto(['../providers/satellite_A/observations.csv','../providers/satellite_B/observations.csv']))
    THEN 'FEDERATED RESULT: COMPLETE'
    ELSE 'FEDERATED RESULT: INCOMPLETE (Missing ground_station)' END;" -noheader
