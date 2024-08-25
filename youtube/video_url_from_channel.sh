yt-dlp -j --flat-playlist "https://www.youtube.com/@anthropic-ai" | jq -r '.id' | sed 's_^_https://youtu.be/_'



# views over 100k and length more than 5 mins
yt-dlp -j --flat-playlist "https://www.youtube.com/@anthropic-ai" | 
jq -r 'select(.view_count != null and .view_count > 100000 and .duration != null and .duration > 300) | "\(.view_count) https://youtu.be/\(.id)"' | 
sort -rn | 
cut -d' ' -f2-


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


# sort by views
 yt-dlp -j --flat-playlist "https://www.youtube.com/@anthropic-ai" | 
                   jq -r 'select(.view_count != null) | "\(.view_count) https://youtu.be/\(.id)"' | 
                   sort -rn | 
                   cut -d' ' -f2-


# views over 50k and length more than 5 mins
yt-dlp -j --flat-playlist "https://www.youtube.com/@anthropic-ai" | 
jq -r 'select(.view_count != null and .view_count > 50000 and .duration != null and .duration > 300) | "\(.view_count) https://youtu.be/\(.id)"' | 
sort -rn | 
cut -d' ' -f2-
