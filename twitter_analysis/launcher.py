import app.processing_functions as pf
import app.bot_1 as b1
import app.bot_2 as b2
import app.bot_3 as b3
import app.sentiment_analysis as sa
import pandas as pd
import app.constants as const
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)


def WordCloud(text_to_visualize):
    try:
        #processed_df = b1.twitter_bot_1()
        #processed_df = b2.twitter_bot_2()
        processed_df = b3.twitter_bot_3()
        return pf.TweetVisualAnalytics(processed_df, text_to_visualize).word_cloud()
    except:
        'smth is wrong'


def launcher_bot_2():
    try:
        list_of_last_20_followings = b2.twitter_bot_2(items_n=5)
        return list_of_last_20_followings
    except:
        'Bot 2 is broken'


def SentimentAnalysis(text_to_analysis):
    try:
        #processed_df = b1.twitter_bot_1()
        #processed_df = b2.twitter_bot_2()
        processed_df = b3.twitter_bot_3()
        return sa.TextDataModel(processed_df, text_to_analysis).sentiment_plot()
    except:
        'smth is wrong'


def main():
    #print(WordCloud('tweet_cleaned'))
    #print(SentimentAnalysis('tweet_cleaned'))
    processed_df = b3.twitter_bot_3(limit=200,result_type='popular')
    #q= const.upcoming_ico

    processed_df.to_json(r'/Users/aminakaltayeva/Desktop/crypto_dvizh/full_tweets_03042022_popular.json')


if __name__ == '__main__':
    main()
