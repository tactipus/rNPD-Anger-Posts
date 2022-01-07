import praw
import pandas as pd
import datetime as dt
import os
import sys
import time
from psaw import PushshiftAPI
import datetime as dt
from sqlalchemy import create_engine

client_id = os.environ.get('CLIENT_ID')
client_secret = os.environ.get('CLIENT_SECRET')
username = os.environ.get('USERNAME')
password = os.environ.get('PASSWORD')

reddit = praw.Reddit(client_id=client_id, \
                     client_secret=client_secret, \
                     user_agent='NPD_Bot/X.X.X', \
                     username=username, \
                     password=password)

NPD = reddit.subreddit("NPD")

topics_dict = { "id": [],
                "title": [],
                "author": [],
                "score": [],
                "time_created": [],
                "comms_num": [],
                "body": [],
                "ups": []
                }

for submission in NPD.search("anger OR angry OR pissed OR upset", limit=1000):
    topics_dict["id"].append(submission.id)
    topics_dict["title"].append(submission.title)
    topics_dict["author"].append(str(submission.author))
    topics_dict["score"].append(submission.score)
    time = int(submission.created_utc)
    topics_dict["time_created"].append(dt.datetime.utcfromtimestamp(time).strftime('%Y-%m-%d %H:%M:%S'))
    topics_dict["comms_num"].append(submission.num_comments)
    topics_dict["body"].append(submission.selftext)
    topics_dict["ups"].append(submission.ups)

topics_data = pd.DataFrame(topics_dict)
engine = create_engine("sqlite:////Users/pnalzate/Documents/GitHub/rNPD_Anger_Posts_Project/instance/r_NPD_Anger.sqlite", echo=False)
topics_data.to_sql('posts', con=engine, if_exists="append", index=False)