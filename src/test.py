if __name__ == '__main__':
    # api = twitter.Api(**twitter_credentials)
    #
    # result = []
    # for i in range(1, 15):
    #     aa = api.GetSearch(raw_query='q=%28salamanca%20OR%20segovia%29&rpp=100&page=' + str(i))
    #
    #     result.append(aa)

    import tweepy
    import csv
    from config.credentials import access_tokens, consumer_keys

    auth = tweepy.OAuthHandler(**consumer_keys)
    auth.set_access_token(access_tokens['access_token_key'], access_tokens['access_token_secret'])

    api = tweepy.API(auth, wait_on_rate_limit=True)

    # Open/Create a file to append data
    csvFile = open('tweets.csv', 'a')
    csvWriter = csv.writer(csvFile)

    # SQL Table columns.
    # -----> tweet_id (using to avoid duplicated tweets)
    # -----> created_at (creation date of tweet)
    # -----> text (tweet content)
    # -----> is_verified (user.verified field to know if tweet ()
    # -----> username (user.name field who wrote tweet)
    # -----> political_party (to join tweet with any political party)

    for tweet in tweepy.Cursor(
            api.search,
            q="%28salamanca%20OR%20segovia%29 -filter:retweets",
            count=100,
            lang="es",
            since="2019-11-30"

    ).items():
        print(tweet.created_at, tweet.text)
        csvWriter.writerow([tweet.created_at, tweet.text.encode('utf-8')])
