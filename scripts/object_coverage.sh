#!/bin/bash
total_providers=$(ls -d ../providers/*/ | wc -l)

# Unikalne ID wewnątrz każdego dostawcy, żeby nie liczyć wielokrotnie u jednego
for file in ../providers/*/observations.csv; do
    cut -d',' -f1 "$file" | sort | uniq
done | sort | uniq -c > /tmp/coverage.txt

echo "=== Obiekty we wszystkich dostawcach ($total_providers) ==="
awk -v tp="$total_providers" '$1 == tp {print $2}' /tmp/coverage.txt

echo "=== Obiekty tylko w jednym dostawcy ==="
awk '$1 == 1 {print $2}' /tmp/coverage.txt
rm /tmp/coverage.txt
