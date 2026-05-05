#!/bin/bash
echo "Rozkład obiektów u dostawców:"
cat ../providers/*/observations.csv | cut -d',' -f1 | sort | uniq -c
