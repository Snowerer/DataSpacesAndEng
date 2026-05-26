#!/bin/bash
echo "Wykrywanie niespójności danych..."
# Wyciągamy same ID, które mają duplikaty (czyli ten sam obiekt u wielu providerów)
cat ../providers/*/observations.csv | sort | uniq | awk -F',' '{print $1}' | sort | uniq -d | while read id; do
    echo "Znaleziono potencjalną niespójność/duplikat dla obiektu $id:"
    grep "^$id," ../providers/*/observations.csv
    echo "---"
done
