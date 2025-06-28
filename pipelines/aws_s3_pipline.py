from etls.aws_etl import create_bucket_if_not_exists, connect_to_s3, upload_to_s3
from utils.constants import AWS_BUCKET_NAME, AWS_KEY


def upload_s3_pipeline(ti):
    file_path = ti.xcom_pull(task_ids='reddit_extraction', key='return_value')
    s3 = connect_to_s3()
    create_bucket_if_not_exists(s3, AWS_BUCKET_NAME)
    aws_key = AWS_KEY +'/'+file_path.split('/')[-1]
    upload_to_s3(s3, file_path, AWS_BUCKET_NAME, aws_key)