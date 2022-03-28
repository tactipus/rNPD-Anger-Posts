import praw
import pandas as pd
import os
import datetime as dt
from sqlalchemy import create_engine
from sqlalchemy import exc

client_id = os.getenv('CLIENT_ID')
client_secret = os.getenv('CLIENT_SECRET')
username = os.getenv('USERNAME')
password = os.getenv('PASSWORD')

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
engine = create_engine("sqlite:////Users/pnalzate/Documents/GitHub/rNPD-Anger-Posts/instance/r_NPD_Anger.sqlite", echo=False)

for i in range(len(topics_data)):
    try:
        topics_data.iloc[i:i + 1].to_sql(name="posts", if_exists='append', con=engine, index=False)
        print("Not a duplicate.")
    except exc.IntegrityError as e:
        print("Integrity Error. Data could not be appended.")
