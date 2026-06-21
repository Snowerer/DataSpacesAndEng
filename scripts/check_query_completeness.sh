#!/bin/bash
OBJ="OBJ-003"

dist_results=$(grep -h "$OBJ" ../providers/*/observations.csv 2>/dev/null | wc -l)

fed_results=0
for meta in ../metadata_catalog/*.json; do
    paths=$(grep -o 'providers/[^"]*\.csv' "$meta")
    for path in $paths; do
        if [ -f "../$path" ]; then
            count=$(grep -c "$OBJ" "../$path")
            fed_results=$((fed_results + count))
        fi
    done
done

echo "Wyszukiwanie rozproszone: $dist_results"
echo "Wyszukiwanie federowane: $fed_results"

if [ "$dist_results" -eq "$fed_results" ]; then
    echo "Wynik: KOMPLETNE"
else
    echo "Wynik: NIEKOMPLETNE"
fi
