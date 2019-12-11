import csv
import sys

import tweepy

sys.path.append("./")
from config.credentials import access_tokens, consumer_keys


def authenticate_twitter():
    auth = tweepy.OAuthHandler(**consumer_keys)
    auth.set_access_token(access_tokens['access_token_key'], access_tokens['access_token_secret'])

    api_ = tweepy.API(auth, wait_on_rate_limit=True)

    return api_


def crawl_tweets(api_):
    cursor = tweepy.Cursor(api_.search,
                           q=f"brexit -filter:retweets",
                           count=100,
                           tweet_mode="extended",
                           lang="en",
                           since="2019-11-28",
                           until="2019-12-10"
                           )

    fieldnames = ['id', 'created_at', 'text', 'username', 'verified']
    with open('tweets.csv', mode='a') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()

        for tweet in cursor.items():
            dto_tweet = {
                'id': tweet.id,
                'created_at': tweet.created_at,
                'text': tweet.full_text,
                'username': tweet.author.screen_name,
                'verified': tweet.author.verified,
            }

            writer.writerow(dto_tweet)


if __name__ == '__main__':
    api = authenticate_twitter()
    crawl_tweets(api)
