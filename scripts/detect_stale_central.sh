#!/bin/bash
for provider_file in ../providers/*/observations.csv; do
    provider_name=$(basename $(dirname "$provider_file"))
    central_file="../central_repository/${provider_name}_observations.csv"
    
    if [ -f "$central_file" ]; then
        if ! cmp -s "$provider_file" "$central_file"; then
            echo "NIEAKTUALNE: $provider_name różni się od kopii centralnej!"
        fi
    else
        echo "BRAK W CENTRALI: $provider_name"
    fi
done
