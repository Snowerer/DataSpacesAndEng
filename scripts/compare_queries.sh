#!/bin/bash
OBJ="OBJ-003"

dist_count=$(./search_distributed.sh "$OBJ" | tail -n 1 | grep -o '[0-9]*')

fed_count=$(./search_federated.sh "$OBJ" | wc -l)

echo "Wynik wyszukiwania rozproszonego: $dist_count"
echo "Wynik wyszukiwania federowanego: $fed_count"

if [ "$dist_count" -eq "$fed_count" ]; then
    echo "Consistency check: yes"
else
    echo "Consistency check: no"
fi
