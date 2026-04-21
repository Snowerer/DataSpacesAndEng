#!/bin/bash
for provider_dir in ../providers/*; do
    provider=$(basename "$provider_dir")
    # Sprawdzamy czy plik JSON istnieje w katalogu metadanych
    if [ -f "../metadata_catalog/${provider}.json" ]; then
        echo "OK: $provider posiada metadane."
    else
        echo "BRAK: $provider nie jest opisany w metadanych!"
    fi
done
