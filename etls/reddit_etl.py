import logging
import pandas as pd
from praw import Reddit
import prawcore
import numpy as np
from utils.constants import POST_FIELDS
logger = logging.getLogger("Reddit-Conn-Logger")
logging.basicConfig(level=logging.INFO)


def connect_reddit(client_id, client_secret, token, user_agent) -> Reddit:
    try:

        reddit = Reddit(
            client_id=client_id,
            client_secret=client_secret,
            refresh_token=token,
            # redirect_uri="http://localhost:8085",
            user_agent=user_agent
        )

        print("Authenticated as:", reddit.user.me())

        logger.info("connected to reddit!")
        return reddit
    except Exception as e:
        logger.error("Exception occured while connecting to reddit")
        return None

def extract_posts(reddit_instance: Reddit,subreddit:str,time_filter:str,limit=None):
    subreddit = reddit_instance.subreddit(subreddit)
    try:
        posts = subreddit.top(time_filter=time_filter, limit=limit)
    except prawcore.exceptions.Forbidden:
        print(f"⛔ Cannot access r/{subreddit.display_name} — skipped entire subreddit")
        return []  # or handle per your ETL strategy

    posts_list = []
    for post in posts:
        post_data = {k: vars(post).get(k) for k in POST_FIELDS}
        posts_list.append(post_data)

    return posts_list

def transform_data(posts_df:pd.DataFrame):
    posts_df['created_utc'] = pd.to_datetime(posts_df['created_utc'],unit='s')
    posts_df['over_18'] = np.where((posts_df['over_18'] == True), True, False)
    posts_df['author'] = posts_df['author'].astype(str)
    # edited_mode = posts_df['edited'].mode()
    if not posts_df['edited'].mode().empty:
        edited_mode = posts_df['edited'].mode().iloc[0]
    else:
        edited_mode = False  # or any default
    posts_df['edited'] = np.where(posts_df['edited'].isin([True, False]),
                                 posts_df['edited'], edited_mode).astype(bool)
    posts_df['num_comments'] = posts_df['num_comments'].astype(int)
    posts_df['score'] = posts_df['score'].astype(int)
    posts_df['title'] = posts_df['title'].astype(str)
    return posts_df

def load_data_to_csv(data: pd.DataFrame, path:str):
    data.to_csv(path, index=False)


if __name__ == '__main__':
    connect_reddit(1,1,'s')


