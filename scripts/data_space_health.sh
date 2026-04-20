#!/bin/bash
REPORT_FILE="../reports/data_space_health.txt"

echo "DATA SPACE HEALTH REPORT" > "$REPORT_FILE"
echo "------------------------" >> "$REPORT_FILE"

total_ds=$(ls ../providers/*/observations.csv 2>/dev/null | wc -l)
echo "Total datasets: $total_ds" >> "$REPORT_FILE"

missing_meta=$(./check_metadata_coverage.sh | grep -c "BRAK")
echo "Missing metadata: $missing_meta" >> "$REPORT_FILE"

empty_ds=$(find ../providers/ -name "observations.csv" -size 0 | wc -l)
echo "Empty datasets: $empty_ds" >> "$REPORT_FILE"

inconsistent_ds=$(./check_metadata_consistency.sh | grep -c "BŁĄD")
echo "Inconsistent datasets: $inconsistent_ds" >> "$REPORT_FILE"

completeness=$(./check_query_completeness.sh | grep -o "KOMPLETNE\|NIEKOMPLETNE" | head -1)
echo "Federated completeness: $completeness" >> "$REPORT_FILE"

echo "Raport zapisany w: $REPORT_FILE"
cat "$REPORT_FILE"
