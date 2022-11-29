# recent tweets searched by users

import pandas as pd
import app.constants as constants
from app.configs import api as api
import app.processing_functions as pf
import datetime


def twitter_bot_1(count_n=100, include_rts=True, t_mode='extended', exclude_replies=True):
    columns = ['tweet_id','influencer', 'created_at', 'full_text']
    full_tweets = pd.DataFrame(columns=columns)

    for i in range(0, len(constants.list_of_influencer_v0)):
        influencer = constants.list_of_influencer_v0[i]
        tweets = api.user_timeline(screen_name=influencer,
                                   count=count_n,
                                   include_rts=include_rts,
                                   tweet_mode=t_mode,
                                   exclude_replies=exclude_replies)
        temp_l1 = pd.DataFrame(columns=columns)

        for tweet in tweets:
            temp_data = []
            temp_data.append([tweet.id, tweet.user.screen_name, tweet.created_at, tweet.full_text])
            temp = pd.DataFrame(temp_data, columns=columns)
            temp_l1 = pd.concat([temp_l1, temp], axis=0)

        full_tweets = pd.concat([full_tweets, temp_l1], axis=0)

    full_tweets = full_tweets.reset_index()
    processed_df = pf.TweetTextProcessing(full_tweets, 'full_text').proccessed_df()
    processed_df['date'] = str(datetime.datetime.now())

    return processed_df
