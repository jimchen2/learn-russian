import subprocess
import os
import uuid

def transcribe_video(video_file):
    output = f"subs_{uuid.uuid4().hex}.vtt"
    subprocess.run([
        'whisper', 
        video_file, 
        '--model', 'medium', 
        '--language', 'ru',  # Set to Russian
        '--output_format', 'vtt',
        '--output_dir', '.', 
    ])
    os.rename(f"{os.path.splitext(video_file)[0]}.vtt", output)
    return output