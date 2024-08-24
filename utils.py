import subprocess
import os

def get_filename_and_extension(url):
    result = subprocess.run(['yt-dlp', '--get-filename', url], capture_output=True, text=True)
    return os.path.splitext(result.stdout.strip())

def cleanup_files(*files):
    for file in files:
        try:
            os.remove(file)
            print(f"Removed: {file}")
        except OSError as e:
            print(f"Error removing {file}: {e}")

def read_urls_from_file(filename):
    with open(filename, 'r') as file:
        return [line.strip() for line in file if line.strip()]