import uuid
import torch
from transformers import MarianMTModel, MarianTokenizer

# Check if CUDA is available
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Using device: {device}")

# Load Helsinki NLP model
model_name = 'Helsinki-NLP/opus-mt-ru-en'
tokenizer = MarianTokenizer.from_pretrained(model_name)
model = MarianMTModel.from_pretrained(model_name).to(device)

def translate_text(text):
    inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True, max_length=512)
    # Move input tensors to the same device as the model
    inputs = {k: v.to(device) for k, v in inputs.items()}
    translated = model.generate(**inputs)
    return tokenizer.decode(translated[0], skip_special_tokens=True)

def translate_vtt(vtt_file):
    translated_vtt = f"translated_{uuid.uuid4().hex}.vtt"

    with open(vtt_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    with open(translated_vtt, 'w', encoding='utf-8') as f:
        f.write("WEBVTT\n\n")
        i = 0
        while i < len(lines):
            line = lines[i].strip()
            if '-->' in line:  # This is a timestamp line
                f.write(line + '\n')
                i += 1
                text_lines = []
                while i < len(lines) and lines[i].strip() and not '-->' in lines[i]:
                    text_lines.append(lines[i].strip())
                    i += 1
                original_text = ' '.join(text_lines)
                translated_text = translate_text(original_text)
                f.write(original_text + '\n')
                f.write(translated_text + '\n\n')
            else:
                i += 1

    return translated_vtt
