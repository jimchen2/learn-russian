#!/bin/bash

# Usage: bash main.sh https://www.youtube.com/watch?v=jubajINJREs

# Check if URL is provided
if [ "$#" -ne 1 ]; then
    echo "Usage: bash main.sh [YouTube URL]"
    exit 1
fi

YOUTUBE_URL=$1

# Step 1: Call download.sh to download video and subtitles
echo "Downloading video and subtitles..."
bash download.sh "$YOUTUBE_URL"

# Read the file paths from download_paths.txt
while IFS= read -r line; do
    if [[ -z "$VIDEO_PATH" ]]; then
        VIDEO_PATH=$line
    elif [[ -z "$ENGLISH_SUB" ]]; then
        ENGLISH_SUB=$line
    elif [[ -z "$RUSSIAN_SUB" ]]; then
        RUSSIAN_SUB=$line
    fi
done < ../videos/download_paths.txt

# Check if files exist
if [[ ! -f "$VIDEO_PATH" || ! -f "$ENGLISH_SUB" || ! -f "$RUSSIAN_SUB" ]]; then
    echo "Error: Missing video or subtitle files."
    exit 1
fi

# Step 2: Call combine_sub.sh to combine the subtitles
echo "Combining subtitles..."
COMBINED_SUB_PATH=$(bash combine_sub.sh "$RUSSIAN_SUB" "$ENGLISH_SUB")

# Step 3: Merge the combined subtitles with the video
echo "Merging subtitles with video..."
mkvmerge -o "${VIDEO_PATH%.webm}_final.mkv" "$VIDEO_PATH" --language 0:en --track-name 0:"English" "$COMBINED_SUB_PATH"

echo "Process completed. Final video with combined subtitles at: ${VIDEO_PATH%.webm}_final.mkv"
rm "$VIDEO_PATH" "$ENGLISH_SUB" "$RUSSIAN_SUB" "$COMBINED_SUB_PATH"  "../videos/download_paths.txt" 
