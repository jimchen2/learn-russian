import os
import boto3
from botocore.exceptions import NoCredentialsError
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

S3_ENDPOINT = os.getenv('S3_ENDPOINT')
S3_ACCESS_KEY = os.getenv('S3_ACCESS_KEY')
S3_SECRET_KEY = os.getenv('S3_SECRET_KEY')
S3_PREFIX = os.getenv('S3_PREFIX', 'processed_video_')
S3_BUCKET=os.getenv('S3_BUCKET', 'processed_video_')

def upload_to_s3(file_name):
    object_name = f"{S3_PREFIX}/{file_name}"

    s3_client = boto3.client('s3',
                             endpoint_url=S3_ENDPOINT,
                             aws_access_key_id=S3_ACCESS_KEY,
                             aws_secret_access_key=S3_SECRET_KEY)

    try:
        s3_client.upload_file(file_name, S3_BUCKET, object_name)
        print(f"Upload Successful: {object_name}")
        return True
    except FileNotFoundError:
        print(f"The file {file_name} was not found")
        return False
    except NoCredentialsError:
        print("Credentials not available")
        return False