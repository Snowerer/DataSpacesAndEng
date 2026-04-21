#!/bin/bash
REPORT_FILE="../reports/data_space_report.txt"

# 1. Total datasets
total_datasets=$(ls ../providers/*/observations.csv 2>/dev/null | wc -l)

# 2. Total records
total_records=0
for file in ../providers/*/observations.csv; do
    count=$(wc -l < "$file")
    total_records=$((total_records + count))
done

# 3. Objects found for query OBJ-003
obj_query="OBJ-003"
obj_found=$(./search_distributed.sh "$obj_query" | tail -n 1 | grep -o '[0-9]*')

# 4. Consistency check
consistency=$(./compare_queries.sh | grep "Consistency check:" | awk '{print $3}')

# Zapis do pliku
{
    echo "DATA SPACE REPORT"
    echo "Total datasets: $total_datasets"
    echo "Total records: $total_records"
    echo "Objects found for query $obj_query: $obj_found"
    echo "Consistency check: $consistency"
} > "$REPORT_FILE"

echo "Raport zapisany w $REPORT_FILE"
