import subprocess
import os
import boto3
from botocore.exceptions import NoCredentialsError
import uuid
import time
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get S3 configuration from environment variables
S3_ENDPOINT = os.getenv('S3_ENDPOINT')
S3_ACCESS_KEY = os.getenv('S3_ACCESS_KEY')
S3_SECRET_KEY = os.getenv('S3_SECRET_KEY')
S3_BUCKET = os.getenv('S3_BUCKET')

def generate_unique_filename(prefix):
    return f"{prefix}_{uuid.uuid4().hex}_{int(time.time())}"

def download_video(url):
    output = f"{generate_unique_filename('video')}.mp4"
    subprocess.run(['yt-dlp', '-o', output, url])
    return output

def transcribe_video(video_file, language):
    output = f"{generate_unique_filename('subs')}_{language}.srt"
    subprocess.run(['whisper', video_file, '--model', 'base', '--language', language, '--output_format', 'srt', '--output_dir', '.'])
    os.rename(f"{os.path.splitext(video_file)[0]}.srt", output)
    return output

def hardcode_subtitles(video_file, subtitle_file):
    output = f"{generate_unique_filename('subtitled')}.mp4"
    subprocess.run(['ffmpeg', '-hwaccel', 'cuda', '-i', video_file, '-vf', f"subtitles={subtitle_file}", '-c:v', 'h264_nvenc', '-c:a', 'copy', output])
    return output

def upload_to_s3(file_name, bucket, object_name=None):
    if object_name is None:
        object_name = os.path.basename(file_name)

    s3_client = boto3.client('s3',
                             endpoint_url=S3_ENDPOINT,
                             aws_access_key_id=S3_ACCESS_KEY,
                             aws_secret_access_key=S3_SECRET_KEY)

    try:
        s3_client.upload_file(file_name, bucket, object_name)
        print(f"Upload Successful: {file_name}")
        return True
    except FileNotFoundError:
        print(f"The file {file_name} was not found")
        return False
    except NoCredentialsError:
        print("Credentials not available")
        return False

def cleanup_files(*files):
    for file in files:
        try:
            os.remove(file)
            print(f"Removed: {file}")
        except OSError as e:
            print(f"Error removing {file}: {e}")

def process_video(url):
    try:
        # Step 1: Download video
        video_file = download_video(url)
        
        # Step 2: Transcribe to English
        english_subs = transcribe_video(video_file, 'en')
        
        # Step 3: Transcribe to Russian
        russian_subs = transcribe_video(video_file, 'ru')
        
        # Step 4: Hardcode English subtitles
        subtitled_video = hardcode_subtitles(video_file, english_subs)
        
        # Step 5: Upload to S3
        upload_to_s3(subtitled_video, S3_BUCKET)
        
        # Clean up
        cleanup_files(video_file, english_subs, russian_subs, subtitled_video)
        
        print(f"Successfully processed and uploaded: {url}")
    except Exception as e:
        print(f"Error processing {url}: {e}")

def read_urls_from_file(filename):
    with open(filename, 'r') as file:
        return [line.strip() for line in file if line.strip()]

def main():
    urls_file = 'video_urls.txt'  # Name of the file containing video URLs
    video_urls = read_urls_from_file(urls_file)
    
    for url in video_urls:
        process_video(url)

if __name__ == "__main__":
    main()
