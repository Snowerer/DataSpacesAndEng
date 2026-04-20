#!/bin/bash
OBJ_ID=${1:-OBJ-003}
TIMESTAMP=$(date +"%Y-%m-%d %H:%M:%S")
FILE_TIME=$(date +"%Y%m%d_%H%M%S")
REPORT_FILE="../reports/query_report_${FILE_TIME}.txt"

{
    echo "DATA SPACE QUERY REPORT"
    echo "Generated at: $TIMESTAMP"
    echo ""
    echo "[GLOBAL STATISTICS]"
    echo -n "Total observations: "
    duckdb -c "SELECT COUNT(*) FROM 'providers/*/observations.csv';" --no-header
    echo -n "Distinct objects: "
    duckdb -c "SELECT COUNT(DISTINCT object_id) FROM 'providers/*/observations.csv';" --no-header
    echo ""
    echo "[OBJECT ANALYSIS: $OBJ_ID]"
    echo "Providers containing object:"
    duckdb -c "SELECT DISTINCT regexp_extract(filename, 'providers/([^/]+)/', 1) FROM read_csv_auto('providers/*/observations.csv', filename=true) WHERE object_id = '$OBJ_ID';" --no-header
    echo -n "Total observations: "
    duckdb -c "SELECT COUNT(*) FROM 'providers/*/observations.csv' WHERE object_id = '$OBJ_ID';" --no-header
    echo ""
    echo "[FEDERATED QUERY COMPARISON]"
    FULL=$(duckdb -c "SELECT COUNT(*) FROM 'providers/*/observations.csv' WHERE object_id = '$OBJ_ID';" --no-header)
    FED=$(duckdb -c "SELECT COUNT(*) FROM read_csv_auto(['providers/satellite_A/observations.csv','providers/satellite_B/observations.csv']) WHERE object_id = '$OBJ_ID';" --no-header)
    echo "FULL RESULT: $FULL"
    echo "FEDERATED RESULT: $FED"
    if [ "$FULL" -eq "$FED" ]; then echo "COMPLETE: YES"; else echo "COMPLETE: NO"; fi
    echo ""
    echo "[SCHEMA VALIDATION]"
    # Porównanie liczby kolumn Satelity A i Ground Station
    COLS_A=$(duckdb -c "DESCRIBE SELECT * FROM 'providers/satellite_A/observations.csv';" | wc -l)
    COLS_GS=$(duckdb -c "DESCRIBE SELECT * FROM 'providers/ground_station/observations.csv';" | wc -l)
    if [ "$COLS_A" -eq "$COLS_GS" ]; then echo "Schema consistency: CONSISTENT"; else echo "Schema consistency: INCONSISTENT"; fi
} | tee $REPORT_FILE

# Wymagany stały plik dla submission
cp $REPORT_FILE ../reports/query_report.txt
