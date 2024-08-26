# Single Video Duration
# ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "https://..."

# Public Bucket
# Base URL: pub-b64e8549cb8d40a082e1f6f1afd4cb58.r2.dev



# BASE_URL="https://pub-b64e8549cb8d40a082e1f6f1afd4cb58.r2.dev"
# TOTAL_DURATION=0

# rclone ls r2:jimchen4214-public | while read -r size object; do
#     duration=$(ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "${BASE_URL}/${object}")
#     printf "%.6f - %s\n" "$duration" "$object"
#     TOTAL_DURATION=$(bc <<<"$TOTAL_DURATION + $duration")
# done

# echo "Total duration: ${TOTAL_DURATION} seconds"


# file is buggy can't use