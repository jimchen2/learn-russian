for dir in $(rclone lsd "r2:jimchen4214-public" | awk '{print $5}'); do
    echo "Size of $dir:"
    rclone size "r2:jimchen4214-public/$dir"
done

echo "Overall Total:"
rclone size "r2:jimchen4214-public"