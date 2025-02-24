#!/bin/bash

# combine_sub.sh
# Usage: bash combine_sub.sh path_to_russian_subtitle path_to_english_subtitle

# Check if both files are provided
if [ "$#" -ne 2 ]; then
    echo "Usage: bash combine_sub.sh path_to_russian_subtitle path_to_english_subtitle"
    exit 1
fi

RUSSIAN_SUB=$1
ENGLISH_SUB=$2
TIMESTAMP=$(date +"%Y%m%d%H%M%S")
COMBINED_SUB="../videos/combined_${TIMESTAMP}.vtt"

# Add VTT header
echo "WEBVTT" > "$COMBINED_SUB"
echo "Kind: captions" >> "$COMBINED_SUB"
echo "Language: en+ru" >> "$COMBINED_SUB"
echo "" >> "$COMBINED_SUB"

# Process Russian subtitles to skip headers
tail -n +4 "$RUSSIAN_SUB" > temp_ru.vtt

# Process English subtitles to skip headers
tail -n +4 "$ENGLISH_SUB" > temp_en.vtt

# Combine the subtitles
awk 'BEGIN {FS="\n"; RS=""; ORS="\n\n"}
     { getline line < "temp_en.vtt"; 
       sub(/^[^\n]+\n[^\n]+\n/, "", line); 
       print $0 "\n" line }' temp_ru.vtt >> "$COMBINED_SUB"

# Remove temporary files
rm temp_ru.vtt temp_en.vtt

# Output the path of the combined subtitles
echo "$COMBINED_SUB"
