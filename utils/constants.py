import configparser
import  os

from pycparser.ply.lex import TOKEN

parser = configparser.ConfigParser()
parser.read(os.path.join(os.path.dirname(__file__), '../config/config.conf'))

SECRET = parser.get('api_keys','reddit_secret_key')
CLIENT_ID = parser.get('api_keys','reddit_client_id')
TOKEN = parser.get('api_keys','reddit_token')

DATABASE_HOST = parser.get('database','database_host')
DATABASE_NAME = parser.get('database','database_name')
DATABASE_PORT = parser.get('database','database_port')
DATABASE_USERNAME = parser.get('database','database_username')
DATABASE_PASSWORD = parser.get('database','database_password')

INPUT_PATH = parser.get('file_paths','input_path')
OUTPUT_PATH = parser.get('file_paths','output_path')

POST_FIELDS = ('id','title','score','num_comments','author','selftext',
     'created_utc','url','over_18',
     'edited','spoiler','stickied')

#AWS
AWS_TOKEN = parser.get('aws','aws_session_token')
AWS_ACCESS_KEY = parser.get('aws','aws_access_key')
AWS_SECRET_KEY = parser.get('aws','aws_secret_key')
AWS_REGION = parser.get('aws','aws_region')
AWS_KEY = parser.get('aws','aws_folder')
AWS_BUCKET_NAME = parser.get('aws','aws_bucket_name')