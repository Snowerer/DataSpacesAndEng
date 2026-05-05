#!/bin/bash
OBJECT_ID=$1
total_matches=0

for file in ../providers/*/observations.csv; do
    if [ -f "$file" ]; then
        # Wypisuje pasujące rekordy
        grep "$OBJECT_ID" "$file"
        
        # Zlicza pasujące rekordy i dodaje do sumy
        count=$(grep -c "$OBJECT_ID" "$file")
        total_matches=$((total_matches + count))
    fi
done
echo "Total matches: $total_matches"
