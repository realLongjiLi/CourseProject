# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
import tweepy
from textblob import TextBlob


class TweetClient:
    def __init__(self):
        consumer_key = 'MILgmh8emE4BLGdBGUIcxivyI'
        consumer_secret = 'u21LcDkCZO5KNAJ5X5sZ5b7yjgZQGa5tefAr15mzxXR7wMYOs9'
        access_token = '1305378037421273088-9ogT0tTfxRcjWbgqZk15BbQKqaRB2V'
        access_token_secret = 'x9Fxxs0wwv6O7dis7qP8oB4V5VnaNPbHhSW8W8GS6tYJJ'
        bearer_token = "AAAAAAAAAAAAAAAAAAAAANUhWgEAAAAAZktLf1kmP4uZg1hjL3Cq3mnrsCQ%3D2ZwkBOR5KkF6IPGRuGq5brYjAazOgpX1RV9Zmb0KbPJWYetYIV"

        try:
            self.client = tweepy.Client(bearer_token=bearer_token, consumer_key=consumer_key, consumer_secret=consumer_secret, access_token=access_token, access_token_secret=access_token_secret)
            print(self.client)
        except Exception as e:
            print("Authentication failed", e)

    def get_tweets(self):
        try:
            tweets = self.client.search_recent_tweets(query="damwon kia", max_results=100)
            data, includes, errors, meta = tweets
            sentiments = [self.analyze_tweet(tweet.text) for tweet in data]
            print(sentiments)
            # for tweet in data:
            #     sentiment = self.analyze_tweet(tweet)
            #     print(sentiment)
            # print(tweets[0]['Response']['data'])
            # for tweet in tweets:
            #     analyze_result = self.analyze_tweet(tweet)

        except Exception as e:
            print("Get tweets failed", e)

    def analyze_tweet(self, tweet):
        analysis = TextBlob(tweet)
        return analysis.sentiment


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    tweetClient = TweetClient()
    tweetClient.get_tweets()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
