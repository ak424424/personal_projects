# Functions for tweet text processing

import pandas as pd
import numpy as np
import emoji as emj
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import re
from app import constants as constants
import string
import nltk
import ssl
try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

words = set(nltk.corpus.words.words())
from googletrans import Translator
trans = Translator()


def remove_emoji(string):
    emoji_pattern = re.compile("["
                               u"\U0001F600-\U0001F64F"  # emoticons
                               u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                               u"\U0001F680-\U0001F6FF"  # transport & map symbols
                               u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                               u"\U00002500-\U00002BEF"  # chinese char
                               u"\U00002702-\U000027B0"
                               u"\U00002702-\U000027B0"
                               u"\U000024C2-\U0001F251"
                               u"\U0001f926-\U0001f937"
                               u"\U00010000-\U0010ffff"
                               u"\u2640-\u2642"
                               u"\u2600-\u2B55"
                               u"\u200d"
                               u"\u23cf"
                               u"\u23e9"
                               u"\u231a"
                               u"\ufe0f"  # dingbats
                               u"\u3030"
                               "]+", flags=re.UNICODE)
    return emoji_pattern.sub(r'', string)


class TweetTextProcessing:

    def __init__(self, df, column_with_tweet):
        self.df = df
        self.column_with_tweet = column_with_tweet

    def precleanup(self):
        df = self.df
        column_with_tweet = self.column_with_tweet

        for index, row in df.iterrows():
            df.loc[index, column_with_tweet] = re.sub(r'\n', ' ', row[column_with_tweet])
        return df

    def extract_emoji(self):
        df = self.precleanup()
        column_with_tweet = self.column_with_tweet
        emojis = emj.UNICODE_EMOJI["en"]

        df['emoji'] = ''
        df['emoji_text'] = ''
        df['tweet_cleaned'] = df[column_with_tweet]
        for index, row in df.iterrows():
            for emoji in emojis:
                if emoji in row[column_with_tweet]:
                    df.loc[index, 'tweet_cleaned'] = remove_emoji(row[column_with_tweet])
                    df.loc[index, 'emoji'] += emoji
            df.loc[index, 'emoji_text'] = emj.demojize(df.loc[index, 'emoji'], delimiters=("", " "))
        return df

    def extract_retweet(self):
        df = self.extract_emoji()
        column_with_tweet = self.column_with_tweet

        df['original_user'] = ''
        for index, row in df.iterrows():
            try:
                df.loc[index, 'original_user'] = re.search('RT @(.*?): ', row[column_with_tweet]).group(1)
                df.loc[index, 'tweet_cleaned'] = re.sub('RT @(.*?): ', ' ', row['tweet_cleaned'])
            except:
                pass
        return df

    def extract_other(self):
        df = self.extract_retweet()
        column_with_text = 'tweet_cleaned'

        df['hashtag'] = ''
        df['mention'] = ''
        df['url'] = ''
        df['currency'] = ''
        for index, row in df.iterrows():
            try:
                df.loc[index, 'hashtag'] = str(re.findall(r"#(\w+)", row[column_with_text]))
                df.loc[index, 'mention'] = str(re.findall(r"@(\w+)", row[column_with_text]))
                df.loc[index, 'url'] = str(re.findall(r"(?P<url>https?://[^\s]+)", row[column_with_text]))
                df.loc[index, 'currency'] = str(re.findall(r"\$(\w+)", row[column_with_text]))
            except:
                pass
        return df

    def clean_tweet_cleaned(self):
        df = self.extract_other()
        combined_pat = r'|'.join((r'(?P<url>https?://[^\s]+)', r'#(\w+)', r"@(\w+)", r"\$(\w+)",
                                  r'&amp;', r'…', r'-'))
        for index, row in df.iterrows():
            df.loc[index, 'tweet_cleaned'] = re.sub(combined_pat, '', row['tweet_cleaned'])
        return df

    def upper_lower_ratio(self):
        df = self.clean_tweet_cleaned()
        column_with_text = 'tweet_cleaned'
        df['upper_lower_ratio'] = ''

        for index, row in df.iterrows():
            upper = 0
            lower = 0

            for i in range(0, len(row[column_with_text])):
                if (row[column_with_text][i] >= 'a' and row[column_with_text][i] <= 'z'):
                    lower += 1
                elif (row[column_with_text][i] >= 'A' and row[column_with_text][i] <= 'Z'):
                    upper += 1
                else:
                    continue

            if lower == 0:
                df.loc[index, 'upper_lower_ratio'] = upper
            else:
                df.loc[index, 'upper_lower_ratio'] = upper / lower
            df.loc[index, 'tweet_cleaned'] = row['tweet_cleaned'].lower()
        return df

    def detect_lang(self):
        df = self.upper_lower_ratio()
        column_with_text = 'tweet_cleaned'

        df['lang'] = ''
        df['tweet_cleaned_en'] = ''

        for index, row in df.iterrows():
            df.loc[index, 'lang'] = str(trans.detect(row[column_with_text]).lang)
            df.loc[index, 'tweet_cleaned_en'] = trans.translate(row[column_with_text]).text
        return df

    def extract_punctuation(self):
        df = self.detect_lang()
        column_with_text = 'tweet_cleaned'
        punctuation = ['!', '?', ':', '.']

        df['punctuation'] = ''

        for index, row in df.iterrows():
            for p in punctuation:
                if p in row[column_with_text]:
                    df.loc[index, 'tweet_cleaned'] = row[column_with_text].translate(str.maketrans('', '',
                                                                                               string.punctuation))
                    df.loc[index, 'tweet_cleaned_en'] = row['tweet_cleaned_en'].translate(str.maketrans('', '',
                                                                                               string.punctuation))
                    df.loc[index, 'punctuation'] += p
        return df

    def dict_non_dict(self):
        df = self.extract_punctuation()
        df['dict_words'] = ''
        df['nondict_words'] = ''

        for index, row in df.iterrows():
            df.loc[index, 'dict_words'] = " ".join(
                w for w in nltk.wordpunct_tokenize(row['tweet_cleaned_en']) if w.lower() in words)
            df.loc[index, 'nondict_words'] = " ".join(
                w for w in nltk.wordpunct_tokenize(row['tweet_cleaned_en']) if w.lower() not in words)
        return df

    def noun_extraction(self):
        df = self.dict_non_dict()
        df['nouns'] = ''

        for index, row in df.iterrows():
            df.loc[index, 'nouns'] = str([word for (word, pos) in
                                          nltk.pos_tag(nltk.word_tokenize(row['tweet_cleaned_en'])) if pos[0] == 'N'])
        return df

    def proccessed_df(self):
        processed_df = self.noun_extraction()
        return processed_df

class TweetVisualAnalytics:

    def __init__(self, df, input_column):
        self.df = df
        self.input = input_column

    def word_cloud(self):
        df = self.df
        column_with_text = self.input

        text_for_cloud = df[column_with_text].str.cat().translate(str.maketrans('', '', string.punctuation))
        word_cloud = WordCloud(width=800, height=400, collocations=False,
                               background_color='white').generate(text_for_cloud)
        plt.figure(figsize=(8, 6))
        plt.imshow(word_cloud)
        plt.axis("off")
        plt.tight_layout(pad=0)
        return plt.show()

    def most_popular_word(self):
        df = self.df
        column_with_text = self.input

        text = df[column_with_text].str.cat().translate(str.maketrans('', '', string.punctuation)).split()
        resultwords = [word for word in text if word.lower() not in constants.stopwords]
        return pd.DataFrame(resultwords, columns=['word']).groupby(['word']).size().reset_index().plot.barh(x='word')
