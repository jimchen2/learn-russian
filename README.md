## Configure `.env`


## Dependencies(on Ubuntu)

```sh
sudo apt update && sudo apt upgrade -y
sudo apt install -y python3-pip python3-venv 
python3 -m venv ~/myenv


source ~/myenv/bin/activate
pip install yt-dlp boto3 uuid python-dotenv
pip install openai-whisper
```

## Clone and Run

```sh
cd ~
git clone https://github.com/jimchen2/whisper-video-s3


cd ~/whisper-video-s3 && source ~/myenv/bin/activate
python run.py
```

## Installing ffmpeg

```sh
#conda uninstall ffmpeg

sudo apt-get update && sudo apt-get install -y build-essential yasm cmake libtool libc6 libc6-dev unzip wget libnuma1 libnuma-dev


cd ~ && wget https://ffmpeg.org/releases/ffmpeg-6.0.tar.xz && tar xJf ffmpeg-6.0.tar.xz && cd ffmpeg-6.0


# nvcc --version
# ls /usr/local/cuda/include
# ls /usr/local/cuda/lib64


# on vastai
# conda install cudatoolkit
# conda update --all

./configure --enable-cuda-nvcc --enable-cuvid --enable-nvenc --enable-nonfree --enable-libnpp --extra-cflags=-I/usr/local/cuda/include --extra-ldflags=-L/usr/local/cuda/lib64


make -j$(nproc) && sudo make install
sudo ldconfig


ffmpeg -version
ffmpeg -hwaccels
```