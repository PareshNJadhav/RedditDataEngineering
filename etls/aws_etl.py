import logging
import s3fs
import boto3
from botocore.exceptions import ClientError
from utils.constants import AWS_ACCESS_KEY, AWS_SECRET_KEY, AWS_REGION

logger = logging.getLogger("aws-logger")
logging.basicConfig(level='INFO')

def connect_to_s3():
    try:
        session = boto3.Session(
            aws_access_key_id=AWS_ACCESS_KEY,
            aws_secret_access_key=AWS_SECRET_KEY,
            #aws_session_token=aws_session_token,  # include only if using STS
            region_name=AWS_REGION
        )

        s3 = session.client('s3')
        return s3
    except Exception as e:
        logger.error(e)
        return None

def create_bucket_if_not_exists(s3:boto3.client,bucket_name):
    try:
        s3.head_bucket(Bucket=bucket_name)
        logger.info(f"✅ Bucket '{bucket_name}' exists.")
    except ClientError as e:
        error_code = e.response['Error']['Code']
        if error_code in ("404", "NoSuchBucket"):
            logger.warning(f"⛔ Bucket '{bucket_name}' does not exist. Creating it...")
            s3.create_bucket(
                Bucket=bucket_name,
                CreateBucketConfiguration={'LocationConstraint': AWS_REGION}
            )
            logger.info(f"✅ Bucket '{bucket_name}' created.")
        else:
            raise

def upload_to_s3(s3:boto3.client,file_path:str, bucket_name:str, s3_key:str):

    try:
        s3.upload_file(file_path, bucket_name, s3_key)
        logger.info(f"✅ file_path '{file_path}' to 's3://{bucket_name}/{s3_key}'")
    except ClientError as e:
        logger.error(f"❌ Failed to upload file: {e}")
        raise
