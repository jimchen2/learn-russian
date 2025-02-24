#!/bin/bash
# download.sh

TIMESTAMP=$(date +"%Y%m%d%H%M%S")
mkdir -p ../videos

# Use yt-dlp to download video and capture the actual file extension
VIDEO_FILE=$(yt-dlp --get-filename -o "../videos/video${TIMESTAMP}.%(ext)s" "$1")
yt-dlp -o "$VIDEO_FILE" "$1"

# Use yt-dlp to download subtitles (english and russian subtitles)
yt-dlp --write-auto-sub --sub-langs "en,ru" --skip-download -o "$VIDEO_FILE" "$1"

# Extract the file extension
EXTENSION="${VIDEO_FILE##*.}"

# Write the file paths to download_paths.txt in the videos folder
echo "${VIDEO_FILE}" > ../videos/download_paths.txt
echo "../videos/video${TIMESTAMP}.en.vtt" >> ../videos/download_paths.txt
echo "../videos/video${TIMESTAMP}.ru.vtt" >> ../videos/download_paths.txt
