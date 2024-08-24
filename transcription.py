import subprocess
import os
import uuid
from transformers import MarianMTModel, MarianTokenizer

# Load Helsinki NLP model
model_name = 'Helsinki-NLP/opus-mt-ru-en'
tokenizer = MarianTokenizer.from_pretrained(model_name)
model = MarianMTModel.from_pretrained(model_name)

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

def translate_text(text):
    inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True, max_length=512)
    translated = model.generate(**inputs)
    return tokenizer.decode(translated[0], skip_special_tokens=True)

def translate_vtt(vtt_file):
    translated_vtt = f"translated_{uuid.uuid4().hex}.vtt"
    
    with open(vtt_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    with open(translated_vtt, 'w', encoding='utf-8') as f:
        for line in lines:
            if line.strip() and not line.strip().replace('->', '').isdigit() and not line.startswith('WEBVTT'):
                translated_line = translate_text(line.strip())
                f.write(f"{line.strip()} [{translated_line}]\n")
            else:
                f.write(line)
    
    return translated_vtt