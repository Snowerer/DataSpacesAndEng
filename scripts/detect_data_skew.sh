#!/bin/bash
wc -l ../providers/*/observations.csv | grep -v "total" | sort -n > /tmp/skew.txt

min_info=$(head -n 1 /tmp/skew.txt)
max_info=$(tail -n 1 /tmp/skew.txt)

min_val=$(echo "$min_info" | awk '{print $1}')
max_val=$(echo "$max_info" | awk '{print $1}')

min_file=$(echo "$min_info" | awk '{print $2}')
max_file=$(echo "$max_info" | awk '{print $2}')

diff=$((max_val - min_val))

echo "Najmniejszy zbiór: $min_file ($min_val rekordów)"
echo "Największy zbiór: $max_file ($max_val rekordów)"
echo "Różnica (skew): $diff"
rm /tmp/skew.txt
