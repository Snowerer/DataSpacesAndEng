#!/bin/bash
for file in ../providers/*/observations.csv; do
    provider=$(basename $(dirname "$file"))
    count=$(wc -l < "$file")
    echo "$provider: $count"
done
