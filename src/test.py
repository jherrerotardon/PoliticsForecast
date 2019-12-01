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
    auth.set_access_token(**access_tokens)

    api = tweepy.API(auth, wait_on_rate_limit=True)
    #####United Airlines
    # Open/Create a file to append data
    csvFile = open('ua.csv', 'a')
    # Use csv Writer
    csvWriter = csv.writer(csvFile)

    for tweet in tweepy.Cursor(api.search, q="#PSOE", count=100,
                               lang="en",
                               since="2019-10-01").items():
        print(tweet.created_at, tweet.text)
        csvWriter.writerow([tweet.created_at, tweet.text.encode('utf-8')])
