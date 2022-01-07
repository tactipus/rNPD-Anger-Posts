# tweepy-bots/bots/config.py
import tweepy as tw
import logging
import os
from dotenv import load_dotenv

logger = logging.getLogger()
load_dotenv(override=True)

consumer_key = os.getenv("CONSUMER_KEY")
consumer_secret = os.getenv("CONSUMER_SECRET")

access_token = os.getenv("ACCESS_TOKEN")
access_token_secret = os.getenv("ACCESS_TOKEN_SECRET")

auth_params = dict(app_key=consumer_key, app_secret=consumer_secret, oauth_token=access_token,
                   oauth_token_secret=access_token_secret)

auth = tw.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)


def create_auth(auth):
    api = tw.API(auth, wait_on_rate_limit=True)

    try:
        api.verify_credentials()
    except Exception as e:
        logger.error("Error creating API", exc_info=True)
        raise e
    logger.info("API created")

    return api
