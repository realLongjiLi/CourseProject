# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
import tweepy
from textblob import TextBlob
import nltk
# nltk.download('vader_lexicon')
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS
import re


class TweetClient:
    def __init__(self):
        # information for api authorization
        consumer_key = 'MILgmh8emE4BLGdBGUIcxivyI'
        consumer_secret = 'u21LcDkCZO5KNAJ5X5sZ5b7yjgZQGa5tefAr15mzxXR7wMYOs9'
        access_token = '1305378037421273088-9ogT0tTfxRcjWbgqZk15BbQKqaRB2V'
        access_token_secret = 'x9Fxxs0wwv6O7dis7qP8oB4V5VnaNPbHhSW8W8GS6tYJJ'
        bearer_token = "AAAAAAAAAAAAAAAAAAAAANUhWgEAAAAAZktLf1kmP4uZg1hjL3Cq3mnrsCQ%3D2ZwkBOR5KkF6IPGRuGq5brYjAazOgpX1RV9Zmb0KbPJWYetYIV"

        try:
            self.client = tweepy.Client(bearer_token=bearer_token, consumer_key=consumer_key, consumer_secret=consumer_secret, access_token=access_token, access_token_secret=access_token_secret)
            self.sid = SentimentIntensityAnalyzer()
        except Exception as e:
            print("Authentication failed", e)

    # fetch tweets from api and parse them
    def get_tweets(self):
        try:
            data, includes, errors, meta = self.client.search_recent_tweets(query="damwon kia", max_results=100)
            return [tweet.text for tweet in data]

        except Exception as e:
            print("Get tweets failed", e)

    # run sentiment analysis on each tweet
    def analyze_tweet(self, tweet):
        analysis = TextBlob(tweet)
        polarity_scores = self.sid.polarity_scores(tweet)
        pos, neg, neu = polarity_scores['pos'], polarity_scores['neg'], polarity_scores['neu']
        if pos > neg:
            attitude = 'pos'
        elif pos < neg:
            attitude = 'neg'
        else:
            attitude = 'neu'
        return analysis.sentiment, attitude


if __name__ == '__main__':
    # initialize the client
    tweetClient = TweetClient()
    # fetch tweets
    tweets = tweetClient.get_tweets()
    # format the tweets
    tweets = [' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t]) |(\w+:\/\/\S+)", " ", tweet).split()) for tweet in
              tweets]
    # run sentiment analysis
    sentiment_analysis = [(tweet, tweetClient.analyze_tweet(tweet)) for tweet in tweets]
    negative = positive = neutral = 0
    positive_tweets = []
    negative_tweets = []
    neutral_tweets = []
    pos_polarized, neg_polarized, neu_polarized = 0, 0, 0
    pos_subjected, neg_subjected, neu_subjected = 0, 0, 0
    for tweet, (sentiment, attitude) in sentiment_analysis:
        if attitude == 'pos':
            positive += 1
            positive_tweets.append(tweet)
            if sentiment.polarity > 0.5:
                pos_polarized += 1
            if sentiment.subjectivity > 0.5:
                pos_subjected += 1
        elif attitude == 'neg':
            negative += 1
            negative_tweets.append(tweet)
            if sentiment.polarity > 0.5:
                neg_polarized += 1
            if sentiment.subjectivity > 0.5:
                neg_subjected += 1
        else:
            neutral += 1
            neutral_tweets.append(tweet)
            if sentiment.polarity > 0.5:
                neu_polarized += 1
            if sentiment.subjectivity > 0.5:
                neu_subjected += 1
    # generate pie graphs
    labels = 'positive posts', 'negative posts', 'neutral posts'
    sizes = [positive, negative, neutral]
    explode = (0, 0.1, 0)
    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%', shadow=True, startangle=90)
    ax1.axis('equal')

    labels = 'positive, polarized', 'positive, nonpolarized', 'negative, polarized', \
             'negative, nonpolarized',  'neutral, polarized', 'neutral, nonpolarized'
    sizes = [pos_polarized, positive - pos_polarized, neg_polarized, negative - neg_polarized, neu_polarized, neutral -
             neu_polarized]
    explode = (0, 0.1, 0, 0, 0, 0)
    fig2, ax2 = plt.subplots()
    ax2.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%', shadow=True, startangle=90)
    ax2.axis('equal')

    labels = 'positive, subjected', 'positive, nonsubjected', 'negative, subjected', \
             'negative, nonsubjected', 'neutral, subjected', 'neutral, nonsubjected'
    sizes = [pos_subjected, positive - pos_subjected, neg_subjected, negative - neg_subjected, neu_subjected, neutral -
             neu_subjected]
    explode = (0, 0.1, 0, 0, 0, 0)
    fig3, ax3 = plt.subplots()
    ax3.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%', shadow=True, startangle=90)
    ax3.axis('equal')

    plt.show()

    # generate word clouds
    wc = WordCloud(background_color='white', stopwords=STOPWORDS | {'RT'})
    wc.generate(''.join(positive_tweets))
    wc.to_file("wc1.png")

    wc.generate(''.join(negative_tweets))
    wc.to_file("wc2.png")

    wc.generate(''.join(neutral_tweets))
    wc.to_file("wc3.png")