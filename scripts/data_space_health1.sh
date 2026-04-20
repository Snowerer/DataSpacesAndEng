#!/bin/bash
echo "ANALYZING DATA SPACE HEALTH..."
# Wywołujemy lokalne skrypty za pomocą ./
SCORE=$(./data_space_coverage.sh | grep "COVERAGE SCORE" | cut -d':' -f2 | tr -d ' %')
DRIFT=$(./schema_drift_detector.sh | grep -c "DRIFT")

if [ "$DRIFT" -gt 0 ]; then
    echo "DATA SPACE HEALTH: CRITICAL (Schema Drift Detected)"
elif (( $(echo "$SCORE < 100" | bc -l) )); then
    echo "DATA SPACE HEALTH: WARNING (Incomplete Coverage: $SCORE%)"
else
    echo "DATA SPACE HEALTH: GOOD"
fi
