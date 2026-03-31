#!/bin/bash
for dataset in ../providers/*/observations.csv; do
    search_path=${dataset#../} # usuwamy ../ z początku do wyszukiwania
    if ! grep -q "$search_path" ../metadata_catalog/*.json 2>/dev/null; then
        echo "OSIEROCONY ZBIÓR: $search_path nie występuje w metadanych!"
    fi
done
