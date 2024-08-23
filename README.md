## Configure `.env`



## Dependencies(on Ubuntu)

```sh
sudo apt update && sudo apt upgrade -y
sudo apt install -y python3-pip python3-venv
sudo add-apt-repository ppa:savoury1/ffmpeg6
sudo apt update
sudo apt install ffmpeg
python3 -m venv ~/myenv


source ~/myenv/bin/activate
pip install yt-dlp boto3 openai-whisper uuid python-dotenv
```


## Run

```
python run.py
```