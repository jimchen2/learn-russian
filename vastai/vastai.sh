conda install -y -c conda-forge ffmpeg=6 cudatoolkit
pip install yt-dlp boto3 uuid python-dotenv transformers openai-whisper sentencepiece sacremoses
sudo apt-get install -y vim
cd ~ && git clone https://github.com/jimchen2/whisper-video-s3 && cd ~/whisper-video-s3 


# Do a Dummy Run to Download Weights(multithreading downloading weights would be disaster)

cat << EOF > video_urls.txt
https://peertube.jimchen.me/w/iSRQZzTpSs2dLtsdMV9Q3d
EOF
python run.py -t 1

# use this to stop errors
# export MKL_THREADING_LAYER=GNU
