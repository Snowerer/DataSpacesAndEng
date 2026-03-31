#!/bin/bash
for meta in ../metadata_catalog/*.json; do
    paths=$(grep -o 'providers/[^"]*\.csv' "$meta")
    for path in $paths; do
        real_path="../$path"
        if [ ! -f "$real_path" ]; then
            echo "BŁĄD: Plik $path wskazany w $meta nie istnieje!"
        elif [ ! -s "$real_path" ]; then
            echo "BŁĄD: Plik $path wskazany w $meta jest pusty!"
        else
            echo "OK: $path jest poprawny."
        fi
    done
done
