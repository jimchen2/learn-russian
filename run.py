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
S3_PREFIX = os.getenv('S3_PREFIX', 'processed_video_') 

def get_filename_and_extension(url):
    result = subprocess.run(['yt-dlp', '--get-filename', url], capture_output=True, text=True)
    return os.path.splitext(result.stdout.strip())

def download_video(url, extension):
    temp_filename = f"temp_{uuid.uuid4().hex}"+extension
    subprocess.run([
        'yt-dlp',
        '-o', temp_filename,
        '-f', 'bestvideo[height<=720]+bestaudio/best[height<=720]',
        '-N', '10',
        url
    ])
    return temp_filename

def transcode_to_mp4(input_file):
    output_file = f"{os.path.splitext(input_file)[0]}.mp4"
    subprocess.run(['ffmpeg', '-hwaccel', 'cuda', '-i', input_file, output_file])
    os.remove(input_file)
    return output_file

def transcribe_video(video_file, language):
    output = f"subs_{uuid.uuid4().hex}_{language}.srt"
    subprocess.run(['whisper', video_file, '--model', 'large', '--language', language, '--output_format', 'srt', '--output_dir', '.'])
    os.rename(f"{os.path.splitext(video_file)[0]}.srt", output)
    return output

def hardcode_subtitles(video_file, subtitle_file):
    output = f"subtitled_{uuid.uuid4().hex}.mp4"
    subprocess.run(['ffmpeg', '-hwaccel', 'cuda', '-i', video_file, '-vf', f"subtitles={subtitle_file}", '-c:v', 'h264_nvenc', '-c:a', 'copy', output])
    return output

def upload_to_s3(file_name, bucket, original_filename):
    object_name = f"{S3_PREFIX}/{original_filename}.mp4"

    s3_client = boto3.client('s3',
                             endpoint_url=S3_ENDPOINT,
                             aws_access_key_id=S3_ACCESS_KEY,
                             aws_secret_access_key=S3_SECRET_KEY)

    try:
        s3_client.upload_file(file_name, bucket, object_name)
        print(f"Upload Successful: {object_name}")
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
        # Get the original filename that yt-dlp would use
        original_filename, extension = get_filename_and_extension(url)

        # Step 1: Download video
        downloaded_video = download_video(url,extension)
        
        # Step 2: Transcode to MP4
        mp4_video = transcode_to_mp4(downloaded_video)
        
        # Step 3: Transcribe to English
        english_subs = transcribe_video(mp4_video, 'en')
        
        # Step 4: Transcribe to Russian
        russian_subs = transcribe_video(mp4_video, 'ru')
        
        # Step 5: Hardcode English subtitles
        subtitled_video = hardcode_subtitles(mp4_video, english_subs)
        
        # Step 6: Upload to S3
        upload_to_s3(subtitled_video, S3_BUCKET, original_filename)
        
        # Clean up
        cleanup_files(mp4_video, english_subs, russian_subs, subtitled_video)
        
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