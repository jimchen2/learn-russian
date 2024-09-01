while IFS= read -r line; do
    if ! grep -q -F "$line" target_file.txt; then
        echo "$line"
    fi
done < video_ids.txt
