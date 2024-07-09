#!/bin/bash

if [ $# -ne 5 ]; then
    echo "Usage: $0 <tumor_sample> <healthy_sample> <regions> <bin_size> <method>"
    exit 1
fi

# Arguments
tumor_sample="$1"
healthy_sample="$2"
regions="$3"
bin_size="$4"
method="$5"

# Run the filtered_depth.sh script with the tumor sample and regions file as arguments
./bin/filtered_depth.sh "$tumor_sample" "$regions" "$bin_size"

# Run the filtered_depth.sh script with the healthy sample and regions file as arguments
./bin/filtered_depth.sh "$healthy_sample" "$regions" "$bin_size"

# Calculate the difference in depth between tumor and healthy samples
python3 bin/compare_depth.py "${tumor_sample%.*}.binnedcounts.tsv" "${healthy_sample%.*}.binnedcounts.tsv" "$method"