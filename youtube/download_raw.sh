mkdir -p temp && cd temp

# # Download videos matching the criteria
# yt-dlp -j --flat-playlist "https://www.youtube.com/openai" |
#     jq -r 'select(.view_count != null and .view_count > 50000 and .duration != null and .duration > 300) | "\(.view_count) https://youtu.be/\(.id)"' |
#     sort -rn | cut -d' ' -f2- | xargs -I {} yt-dlp {}




# 720p
yt-dlp -j --flat-playlist "https://www.youtube.com/openai" |
    jq -r 'select(.view_count != null and .view_count > 50000 and .duration != null and .duration > 300) | "\(.view_count) https://youtu.be/\(.id)"' |
    sort -rn | cut -d' ' -f2- | xargs -I {} yt-dlp -f 'bestvideo[height<=720][ext=webm]+bestaudio[ext=webm]/best[height<=720][ext=webm]/best[ext=webm]' {}



# Use rclone to upload the directory
rclone copy . r2:bucket/prefix/
