# recent following searched by users

import tweepy
import pandas as pd
import app.constants as constants
from app.configs import api as api
import datetime


def twitter_bot_2(items_n=200000):
    list_of_followings = pd.DataFrame()

    for i in range(0, len(constants.list_of_influencer_v0)):
        influencer = constants.list_of_influencer_v0[i]
        temp = pd.DataFrame(columns=constants.characteristics_users)

        p = 0

        for friend in tweepy.Cursor(api.get_friends, screen_name=influencer).items(items_n):
            temp.loc[p] = ([friend.screen_name] + [friend.description] + [friend.created_at] +
                           [friend.followers_count] + [friend.friends_count] + [friend.listed_count] +
                           [friend.favourites_count] + [friend.location] + [friend.verified])
            p += 1

        temp['influencer'] = influencer
        list_of_followings = pd.concat([list_of_followings, temp], axis=0)
        list_of_followings['date'] = str(datetime.datetime.now())

    return list_of_followings
