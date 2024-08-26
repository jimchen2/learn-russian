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
import re
import glob

# Load environment variables from .env file
load_dotenv()


def download_video(url):
    # Generate a UUID
    file_uuid = uuid.uuid4().hex
    print(f"Generated UUID: {file_uuid}")

    # Run yt-dlp with the UUID as part of the filename

    command = [
        'yt-dlp',
        '-f', 'bestvideo[height<=720]+bestaudio/best[height<=720]/best',
        '-N', '20',
        "-o", f"{file_uuid}.%(ext)s",
        url
    ]
    print(f"Executing command: {' '.join(command)}")

    process = subprocess.Popen(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        universal_newlines=True
    )
    
    # Print output in real-time
    while True:
        output = process.stdout.readline()
        if output == '' and process.poll() is not None:
            break
        if output:
            print(output.strip())

    process.wait()
    print(f"yt-dlp process completed with return code: {process.returncode}")

    # Search for the file with the UUID in the current directory
    matching_files = glob.glob(f'{file_uuid}.*')

    if matching_files:
        downloaded_file = matching_files[0]
        print(f"File downloaded: {downloaded_file}")
        return downloaded_file
    else:
        print("File not found after download.")
        return None    
    
def transcode_to_mp4(input_file):
    if input_file.lower().endswith('.mp4'):
        print(f"File {input_file} is already an MP4. Skipping transcoding.")
        return input_file

    output_file = f"{os.path.splitext(input_file)[0]}.mp4"

    try:
        probe = subprocess.check_output(['ffprobe', '-v', 'error', '-select_streams', 'v:0', 
                                         '-count_packets', '-show_entries', 'stream=width,height,r_frame_rate', 
                                         '-of', 'csv=p=0', input_file]).decode('utf-8').strip().split(',')
        width, height, fps = probe
        width, height = map(int, (width, height))
        fps = eval(fps)  # r_frame_rate is returned as a fraction, e.g., '30000/1001'
    except subprocess.CalledProcessError:
        print(f"Error: Unable to probe {input_file}")
        return input_file

    vf_filters = []

    # Resize to 720p if original is larger
    if height > 720:
        vf_filters.append(f'scale=-1:720')

    # Reduce frame rate if higher than 30 fps
    if fps > 30:
        vf_filters.append('fps=30')

    vf_string = ','.join(vf_filters)

    command = [
        'ffmpeg',
        '-hwaccel', 'cuda',
        '-i', input_file,
        '-c:v', 'libx264',
        '-c:a', 'aac',
        '-b:a', '128k'
    ]

    if vf_filters:
        command.extend(['-vf', vf_string])

    command.append(output_file)

    try:
        subprocess.run(command, check=True)
        os.remove(input_file)
        print(f"Transcoded to {output_file}")
        return output_file
    except subprocess.CalledProcessError as e:
        print(f"Error transcoding {input_file}: {e}")
        return input_file

def process_and_upload_video(url):
    try:
        # Get the original filename that yt-dlp would use
        original_filename, _ = get_filename_and_extension(url)

        print(original_filename)

        # Step 1: Download video
        downloaded_video = download_video(url)

        print(downloaded_video)
        
        # Step 2: Transcode to MP4
        mp4_video = transcode_to_mp4(downloaded_video)

        print(mp4_video)
        
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
        
        # Clean up temporary files
        if os.path.exists(mp4_video):
            os.remove(mp4_video)
        if os.path.exists(russian_subs):
            os.remove(russian_subs)
        if os.path.exists(translated_subs):
            os.remove(translated_subs)
        if os.path.exists(subtitled_video):
            os.remove(subtitled_video)
        
        return None  # No error occurred
    except Exception as e:
        print(f"Error processing and uploading {url}: {e}")
        return url  # Return the URL that caused an error
    finally:
        # Ensure downloaded_video is always removed, even if an exception occurs
        if 'downloaded_video' in locals() and os.path.exists(downloaded_video):
            os.remove(downloaded_video)

def main():
    parser = argparse.ArgumentParser(description="Process and upload videos with multithreading.")
    parser.add_argument('-t', '--threads', type=int, default=1, help="Number of threads to use (default: 1)")
    args = parser.parse_args()

    urls_file = 'video_urls.txt'  # Name of the file containing video URLs
    video_urls = list(set(line.strip() for line in open(urls_file) if line.strip()))   
     
    with ThreadPoolExecutor(max_workers=args.threads) as executor:
        executor.map(process_and_upload_video, video_urls)

if __name__ == "__main__":
    main()