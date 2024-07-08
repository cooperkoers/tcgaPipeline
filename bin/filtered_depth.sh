#!/bin/bash

if [ $# -ne 2 ]; then
    echo "Usage: $0 <sample> <regions>"
    exit 1
fi

# Arguments
sample="$1"
regions="$2"

# Temporary files
sorted=$(mktemp)
depth=$(mktemp)
bed=$(mktemp)

# Sort BAM file
echo "sorting BAM file..."
samtools sort -o "$sorted" "$sample"

# Index BAM file
echo "indexing BAM file..."
samtools index "$sorted"

# Calculate depth
echo "calculating positional depth..."
samtools depth "$sorted" > "$depth"

# Convert depth file into a BED file
echo "converting depth file into bed file..."
awk '{print $1"\t"$2"\t"$2+1"\t"$3}' "$depth" > "$bed"

# Subtract regions from BED file and save the final output
output="${sample%.*}.subtracted.bed"
echo "subtracting regions from bed file..."
bedtools subtract -a "$bed" -b "$regions" > "$output"

# Clean up temporary files
rm "$sorted" "$depth" "$bed" "${sorted}.bai"

echo "Depth calculation complete. Subtracted BED file saved to: $output"

