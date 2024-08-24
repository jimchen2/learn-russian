conda install -c conda-forge ffmpeg=6 cudatoolkit
pip install yt-dlp boto3 uuid python-dotenv transformers openai-whisper sentencepiece sacremoses
apt install vim


cd ~ && git clone https://github.com/jimchen2/whisper-video-s3 && cd ~/whisper-video-s3 

# use this to stop errors
# export MKL_THREADING_LAYER=GNU
