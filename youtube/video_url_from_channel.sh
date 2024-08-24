yt-dlp -j --flat-playlist "https://www.youtube.com/@anthropic-ai" | jq -r '.id' | sed 's_^_https://youtu.be/_'



# filter out videos more than 2 mins
yt-dlp -j --flat-playlist "https://www.youtube.com/@anthropic-ai" | 
jq 'select(.duration != null and .duration > 120) | .id' -r | 
sed 's_^_https://youtu.be/_'

# non-live
yt-dlp -j --flat-playlist "https://www.youtube.com/@anthropic-ai" | 
jq 'select(.live_status == null) | .id' -r | 
sed 's_^_https://youtu.be/_'


# non-live and more than 2 mins
yt-dlp -j --flat-playlist "https://www.youtube.com/@anthropic-ai" | 
jq 'select(.live_status == null and .duration != null and .duration > 120) | .id' -r | 
sed 's_^_https://youtu.be/_'


# live
yt-dlp -j --flat-playlist "https://www.youtube.com/@anthropic-ai" | 
jq 'select(.live_status == "was_live") | .id' -r | 
sed 's_^_https://youtu.be/_'


