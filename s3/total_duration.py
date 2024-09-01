import subprocess
import re
import argparse
from urllib.parse import quote
from concurrent.futures import ThreadPoolExecutor

BASE_URL = "https://pub-b64e8549cb8d40a082e1f6f1afd4cb58.r2.dev"

def run_cmd(cmd):
    return subprocess.run(cmd, capture_output=True, text=True).stdout

def get_duration(url):
    try:
        return float(run_cmd(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", url]))
    except:
        return 0

def process_video(line):
    match = re.search(r'(\d+)\s+(.+\.(mp4|avi|mov|mkv|webm|flv|wmv|m4v))$', line)
    if match:
        object_name = match.group(2)
        encoded_name = quote(object_name)
        try:
            duration = get_duration(f"{BASE_URL}/{encoded_name}")
            return duration, object_name, encoded_name
        except Exception as e:
            print(f"Error processing {object_name}: {e}")
    return 0, None, None

def main(bucket_name, threads):
    total_duration = 0
    processed_files = 0

    with ThreadPoolExecutor(max_workers=threads) as executor:
        futures = []
        for line in run_cmd(["rclone", "ls", f"r2:{bucket_name}"]).splitlines():
            futures.append(executor.submit(process_video, line))

        for future in futures:
            duration, object_name, encoded_name = future.result()
            if object_name:
                total_duration += duration
                processed_files += 1
                print(f"{duration:.6f} - {object_name}")
                print(f"Encoded URL: {BASE_URL}/{encoded_name}")
                print(f"Current total duration: {total_duration:.6f}")
                print(f"Processed files: {processed_files}\n")

    print(f"Total duration: {total_duration:.6f} seconds")
    print(f"Total processed files: {processed_files}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process video files in an S3 bucket concurrently.")
    parser.add_argument("--bucket_name", help="Name of the S3 bucket", default="jimchen4214-public")
    parser.add_argument("-t", "--threads", type=int, default=10, help="Number of threads to use")
    args = parser.parse_args()

    main(args.bucket_name, args.threads)