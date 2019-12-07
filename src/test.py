parties_query = {
        'PSOE': 'PSOE',
        'PP': 'PP',
        'Cs': 'Ciudadanos',
        'UP': 'Unidas podemos',
        'Vox': 'Vox'
    }

def CrawlPartyTweets(party):
    cursor = tweepy.Cursor(api.search,
        q=f"{parties_query[party]} -filter:retweets",
        count=100,
        tweet_mode="extended",
        lang="es",
        since="2019-11-28",
        until="2019-12-10"
    )
    for tweet in cursor.items():
        dto_tweet = {
            'id': tweet.id,
            'created_at': tweet.created_at,
            'text': tweet.full_text,
            'username': tweet.author.screen_name,
            'verified': tweet.author.verified,
            'political_party': 'PSOE'
        }
        values = ", ".join("'" + str(x) + "'" for x in dto_tweet.values()).replace('\\', '')
        insert = f'INSERT INTO tweets VALUES({values})'
        try :
            db.execute(insert)
        except Exception as e:
            print(e)
            pass
        db.commit()

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
    import sys
    import pyodbc
    sys.path.append("./")
    from config.credentials import access_tokens, consumer_keys

    auth = tweepy.OAuthHandler(**consumer_keys)
    auth.set_access_token(access_tokens['access_token_key'], access_tokens['access_token_secret'])

    api = tweepy.API(auth, wait_on_rate_limit=True)

    # SQL Table columns.
    # -----> id (using to avoid duplicated tweets)
    # -----> created_at (creation date of tweet)
    # -----> text (tweet content)
    # -----> verified (author.verified field to know if tweet ()
    # -----> username (author.screen_name field who wrote tweet)
    # -----> political_party (to join tweet with any political party)
    conn = pyodbc.connect(
        'Driver={SQL Server};'
        'Server=LOCALHOST\SQLEXPRESS;'
        'Database=Political_forecast;'
        'Trusted_Connection=yes;'
    )
    db = conn.cursor()
    for key in parties_query.keys():
        CrawlPartyTweets(key)