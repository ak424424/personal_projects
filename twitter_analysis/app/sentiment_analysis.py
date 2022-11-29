from textblob import TextBlob
import matplotlib.pyplot as plt


class TextDataModel:

    def __init__(self, df, column_with_text):
        self.df = df
        self.column_with_text = column_with_text

    def subjectivity(self, text):
        return TextBlob(text).sentiment.subjectivity

    def polarity(self, text):
        return TextBlob(text).sentiment.polarity

    def sentiment(self, score):
        if score < 0:
            return 'negative'
        elif score == 0:
            return 'neutral'
        else:
            return 'positive'

    def sentiment_plot(self):
        df = self.df
        text = self.column_with_text

        df['subjectivity'] = df[text].apply(self.subjectivity)
        df['polarity'] = df[text].apply(self.polarity)
        df['sentiment'] = df['polarity'].apply(self.sentiment)

        plt.figure(figsize=(8, 6))
        for i in range(0, df.shape[0]):
            plt.scatter(df['polarity'][i], df['subjectivity'][i], color='Purple')
        plt.title('Sentiment Analysis Scatter Plot')
        plt.xlabel('Polarity')
        plt.ylabel('Subjectivity')
        return plt.show(), df


