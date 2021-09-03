import twitter
import sys
import pandas as pd


TWITTER_API = twitter.Api(consumer_key='',
                  consumer_secret='',
                  access_token_key='',
                  access_token_secret='',
                  tweet_mode='extended')


def get_tweets(screen_name, to_csv=True):
    """Get the last 3200 tweets from a given twitter user and output them to a csv file
    This code has been taken and modified from the python-twitter api examples found here:z
    https://github.com/bear/python-twitter

    :return: dataframe ['created_at', 'text']
    """
    timeline = TWITTER_API.GetUserTimeline(screen_name=screen_name, count=200)
    earliest_tweet = min(timeline, key=lambda x: x.id).id
    df = None
    print("Getting user: {}".format(screen_name))
    print("--> getting tweets before:", earliest_tweet)

    while True:
        tweets = TWITTER_API.GetUserTimeline(
            screen_name=screen_name, max_id=earliest_tweet, count=200
        )
        new_earliest = min(tweets, key=lambda x: x.id).id

        if not tweets or new_earliest == earliest_tweet:
            break
        else:
            earliest_tweet = new_earliest
            print("--> getting tweets before:", earliest_tweet)
            timeline += tweets

        manifest = []
        for tweet in timeline:
            t = tweet.AsDict()
            manifest.append({'created_at': t['created_at'], 'text': t['full_text']})

        df = pd.DataFrame(manifest)
        if to_csv:
            df.to_csv("{}.csv".format(screen_name), index=False, header=True)
    return df


if __name__ == '__main__':
    file_name = sys.argv[1]
    users = pd.read_csv(file_name, sep=',')
    users['screen_name'].apply(get_tweets)
