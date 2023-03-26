#!/bin/bash
index=$(curl "https://www.investing.com/indices/volatility-s-p-500")
index=$( echo "$index" | grep -oP '<span class="text-2xl" data-test="instrument-price-last">.*</span>' | grep -oE '[0-9]+\.[0-9]+' | head -n 1)

echo "$index" >> vix.txt
echo "$(date)" >> vix_date.txt
