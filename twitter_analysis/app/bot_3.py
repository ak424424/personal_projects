# recent tweets searched by keywords

import tweepy
import pandas as pd
import datetime
import app.constants as constants
from app.configs import api as api
#import app.processing_functions as pf


def twitter_bot_3(q=constants.keywords, geocode=None, count_n=100, t_mode='extended', result_type='mixed', limit=1000):
    columns = ['tweet_id', 'user', 'location', 'created_at', 'full_text', 'result_type', 'iso_lang', 'rt_tweet_id',
               'rt_user', 'rt_follower_count', 'rt_friends_count', 'rt_listed_count', 'rt_created_at', 'rt_location',
               'rt_retweet_count', 'rt_favourite_count']
    full_tweets = pd.DataFrame(columns=columns)

    for i in range(0, len(q)):
        keyword = q[i]
        temp_l1 = pd.DataFrame(columns=columns)
        for tweet in tweepy.Cursor(api.search_tweets, q=keyword,
                               count=count_n,
                               tweet_mode=t_mode,
                               result_type=result_type).items(limit):
            temp = []
            try:
                temp.append([tweet.id, tweet.user.screen_name, tweet.user.location, tweet.created_at, tweet.full_text,
                             tweet.metadata['result_type'], tweet.metadata['iso_language_code'],
                             tweet.retweeted_status.id,
                             tweet.retweeted_status.user.screen_name, tweet.retweeted_status.user.followers_count,
                             tweet.retweeted_status.user.friends_count, tweet.retweeted_status.user.listed_count,
                             tweet.retweeted_status.user.created_at, tweet.retweeted_status.user.location,
                             tweet.retweeted_status.retweet_count, tweet.retweeted_status.favorite_count])
            except:
                temp.append([tweet.id, tweet.user.screen_name, tweet.user.location, tweet.created_at, tweet.full_text,
                             tweet.metadata['result_type'], tweet.metadata['iso_language_code'],
                             'na', 'na', 'na', 'na', 'na', 'na', 'na', 'na', 'na'])

            temp = pd.DataFrame(temp, columns=columns)
            temp_l1 = pd.concat([temp_l1, temp], axis=0)

        temp_l1['keyword'] = keyword
        full_tweets = pd.concat([full_tweets, temp_l1], axis=0)
        print(str(keyword) + ' - done - ' + str(datetime.datetime.now()))

    full_tweets = full_tweets.reset_index().drop(columns=['index'])
    #processed_df = TweetTextProcessing(full_tweets, 'full_text').proccessed_df()
    full_tweets['date'] = str(datetime.datetime.now())
    return full_tweets#processed_df
