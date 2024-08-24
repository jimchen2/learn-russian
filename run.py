import os
import subprocess
import uuid
import argparse
from concurrent.futures import ThreadPoolExecutor
from dotenv import load_dotenv
from s3_operations import upload_to_s3
from transcription import transcribe_video
from translation import translate_vtt
from utils import read_urls_from_file, get_filename_and_extension
from write_subtitles import process_video

# Load environment variables from .env file
load_dotenv()

def download_video(url, extension):
    temp_filename = f"temp_{uuid.uuid4().hex}"+extension
    subprocess.run([
        'yt-dlp',
        '-o', temp_filename,
        '-f', 'bestvideo[height<=720]+bestaudio/best[height<=720]',
        '-N', '100',
        url
    ])
    return temp_filename

def transcode_to_mp4(input_file):
    # Check if the input file is already an MP4
    if input_file.lower().endswith('.mp4'):
        print(f"File {input_file} is already an MP4. Skipping transcoding.")
        return input_file

    output_file = f"{os.path.splitext(input_file)[0]}.mp4"
    probe = subprocess.check_output(['ffprobe', '-v', 'error', '-select_streams', 'v:0', 
                                     '-count_packets', '-show_entries', 'stream=width,height', 
                                     '-of', 'csv=p=0', input_file]).decode('utf-8').strip().split(',')
    width, height = map(int, probe)

    # Calculate target dimensions
    target_height = height
    target_width = height * 16 // 9
    
    if target_width < width:
        target_width = width
        target_height = width * 9 // 16

    # Construct FFmpeg command
    command = [
        'ffmpeg',
        '-hwaccel', 'cuda',  # Use CUDA hardware acceleration
        '-i', input_file,
        '-vf', f'pad={target_width}:{target_height}:(ow-iw)/2:(oh-ih)/2',
        '-c:v', 'h264_nvenc',  # Use NVIDIA NVENC encoder
        '-preset', 'p4',  # Fastest preset for NVENC
        '-tune', 'hq',  # High quality tuning
        '-b:v', '5M',  # Set a target bitrate (adjust as needed)
        '-maxrate', '10M',  # Maximum bitrate
        '-bufsize', '15M',  # VBV buffer size
        '-c:a', 'copy',  # Copy audio without re-encoding
        output_file
    ]
    
    subprocess.run(command)
    os.remove(input_file)
    print(f"Transcoded to {output_file}")
    return output_file

def process_and_upload_video(url):
    try:
        # Get the original filename that yt-dlp would use
        original_filename, extension = get_filename_and_extension(url)

        # Step 1: Download video
        downloaded_video = download_video(url, extension)
        
        # Step 2: Transcode to MP4
        mp4_video = transcode_to_mp4(downloaded_video)
        
        # Step 3: Transcribe to Russian
        russian_subs = transcribe_video(mp4_video)
        
        # Step 4: Translate Russian VTT to English and combine
        translated_subs = translate_vtt(russian_subs)
        
        # Step 5: Process video (add subtitles)
        subtitled_video = process_video(mp4_video, translated_subs, original_filename)
        
        if subtitled_video:
            # Step 6: Upload to S3
            print(subtitled_video)
            upload_to_s3(subtitled_video)
            print(f"Successfully uploaded: {original_filename}")
        
        # Clean up temporary files
        if os.path.exists(mp4_video):
            os.remove(mp4_video)
        if os.path.exists(russian_subs):
            os.remove(russian_subs)
        if os.path.exists(translated_subs):
            os.remove(translated_subs)
        if os.path.exists(subtitled_video):
            os.remove(subtitled_video)
        
    except Exception as e:
        print(f"Error processing and uploading {url}: {e}")
    finally:
        # Ensure downloaded_video is always removed, even if an exception occurs
        if 'downloaded_video' in locals() and os.path.exists(downloaded_video):
            os.remove(downloaded_video)

def main():
    parser = argparse.ArgumentParser(description="Process and upload videos with multithreading.")
    parser.add_argument('-t', '--threads', type=int, default=1, help="Number of threads to use (default: 1)")
    args = parser.parse_args()

    urls_file = 'video_urls.txt'  # Name of the file containing video URLs
    video_urls = read_urls_from_file(urls_file)
    
    with ThreadPoolExecutor(max_workers=args.threads) as executor:
        executor.map(process_and_upload_video, video_urls)

if __name__ == "__main__":
    main()