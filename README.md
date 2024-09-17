*I am going to hoard only annually, so the next time I am expected to hoard at February next year.*

*Also next time I hoard I will archive some videos to another bucket, sort of like creating a buffer space*

## 2024.09.18

Public Bucket

- Total size: 415.520 GiB (446161095352 Byte)
- Total duration: 4902331.463317 seconds (1360 hours)

## 2024.09.02

Public Bucket

- Total size: 333.062 GiB (357622904912 Byte)
- Total duration: 3523849.461206 seconds (978 hours)

## 2024.08.27

Public Bucket

- Total size: 126.058 GiB (135353908926 Byte)
- Total duration: 1471226.817983 seconds (408 hours)

This is the first time I hoarded.
 
*Incident: I configured Cloudflare to delete object after one day, which fucked everything up.*

## ToDo

Support Multi-GPU

1. First run a dummy to download the weights

2. 3 threads is a good utilization of GPU

3. Run the test in `video_urls` for different platforms

4. Configure `.env`

See `~/.config/rclone/rclone.conf`

5. Configure `video_urls.txt`

## Install

```sh
sudo apt update && sudo apt upgrade -y
sudo apt install -y python3-pip python3-venv
python3 -m venv ~/myenv
source ~/myenv/bin/activate
pip install yt-dlp boto3 uuid python-dotenv openai-whisper

## Clone and Run

source ~/myenv/bin/activate
cd ~
git clone https://github.com/jimchen2/whisper-video-s3


cd ~/whisper-video-s3
python run.py -t 1

## Installing ffmpeg

# on vastai
# conda install -c conda-forge ffmpeg=6 cudatoolkit

# Verify
ffmpeg -hwaccels
```
