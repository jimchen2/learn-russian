import os
import subprocess

def add_subtitles_to_video(video_file, subtitle_file, output_file):
    command = [
        'ffmpeg',
        '-hwaccel', 'cuda',  # Use CUDA hardware acceleration
        '-i', video_file,
        '-vf', f'subtitles={subtitle_file}',
        '-c:v', 'h264_nvenc',  # Use NVIDIA GPU encoding for output
        '-c:a', 'copy',
        '-threads', '0',  # Use all available CPU threads
        '-preset', 'fast',  # Use a faster encoding preset
        output_file
    ]
    subprocess.run(command, check=True)

def process_video(video_file, subtitle_file, original_filename):
    print(video_file,subtitle_file,original_filename)
    try:
        # Add subtitles to the video
        output_file = f"{original_filename}.mp4"
        add_subtitles_to_video(video_file, subtitle_file, output_file)

        # Clean up temporary files
        os.remove(video_file)
        os.remove(subtitle_file)

        print(f"Successfully processed: {original_filename}")
        return output_file
    except Exception as e:
        print(f"Error processing {original_filename}: {e}")
        return None