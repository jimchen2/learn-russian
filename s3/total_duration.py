import subprocess, re, argparse
from urllib.parse import quote
from concurrent.futures import ThreadPoolExecutor, as_completed

BASE_URL = "https://pub-b64e8549cb8d40a082e1f6f1afd4cb58.r2.dev"

def run_cmd(cmd):
    return subprocess.run(cmd, capture_output=True, text=True).stdout

def get_duration(url):
    return float(run_cmd(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", url]))

def process_video(line):
    match = re.search(r'(\d+)\s+(.+\.(mp4|avi|mov|mkv|webm|flv|wmv|m4v))$', line)
    if match:
        object_name = match.group(2)
        encoded_name = quote(object_name)
        try:
            duration = get_duration(f"{BASE_URL}/{encoded_name}")
            return duration, object_name, encoded_name
        except Exception as e:
            print(f"Error processing {object_name}: {str(e)}")
    return 0, None, None

def main(threads):
    total_duration = 0
    with ThreadPoolExecutor(max_workers=threads) as executor:
        for duration, object_name, encoded_name in executor.map(process_video, run_cmd(["rclone", "ls", "r2:jimchen4214-public/"]).splitlines()):
            if object_name:
                total_duration += duration
                print(f"{duration:.6f} - {object_name}")
                print(f"Encoded URL: {BASE_URL}/{encoded_name}")
                print(f"Current total duration: {total_duration:.6f}\n")
    print(f"Total duration: {total_duration:.6f} seconds")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process video files concurrently.")
    parser.add_argument("-t", "--threads", type=int, default=1, help="Number of threads to use")
    main(parser.parse_args().threads)