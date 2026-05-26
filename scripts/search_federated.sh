#!/bin/bash
OBJECT_ID=$1

for meta in ../metadata_catalog/*.json; do
    # Wyciągamy ścieżki z plików JSON
    paths=$(grep -o 'providers/[^"]*\.csv' "$meta")
    for path in $paths; do
        if [ -f "../$path" ]; then
            grep "$OBJECT_ID" "../$path"
        fi
    done
done
