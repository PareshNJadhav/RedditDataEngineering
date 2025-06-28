from etls.reddit_etl import connect_reddit, extract_posts, transform_data, load_data_to_csv
from utils.constants import CLIENT_ID,SECRET,OUTPUT_PATH,TOKEN
import pandas as pd

def reddit_pipeline(file_name:str,subreddit:str,timefilter:str='day',limt:int=None):
    #connecting to reddit
    reddit_instance = connect_reddit(CLIENT_ID,SECRET,TOKEN,'request by u/pj34892')
    #extraction
    posts = extract_posts(reddit_instance,subreddit,timefilter,limt)
    post_df =pd.DataFrame(posts)
    #transformation
    post_df = transform_data(post_df)
    #loading to csv
    file_path = f'{OUTPUT_PATH}/{file_name}.csv'
    load_data_to_csv(post_df,file_path)

    return  file_path
