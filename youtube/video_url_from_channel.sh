yt-dlp -j --flat-playlist "https://www.youtube.com/@anthropic-ai" | jq -r '.id' | sed 's_^_https://youtu.be/_'



# filter out videos less than 2 mins
yt-dlp -j --flat-playlist "https://www.youtube.com/@anthropic-ai" | 
jq 'select(.duration != null and .duration > 120) | .id' -r | 
sed 's_^_https://youtu.be/_'