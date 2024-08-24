import os
from dotenv import load_dotenv
from video_processing import process_video
from utils import read_urls_from_file

# Load environment variables from .env file
load_dotenv()

def main():
    urls_file = 'video_urls.txt'  # Name of the file containing video URLs
    video_urls = read_urls_from_file(urls_file)
    
    for url in video_urls:
        process_video(url)

if __name__ == "__main__":
    main()