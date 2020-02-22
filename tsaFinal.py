import re

import tweepy
from pytrends.request import TrendReq
from textblob import TextBlob
from tweepy import OAuthHandler


def clean_tweet(tweet):
    return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t]) |(\w+:\/\/\S+)", " ", tweet).split())


def get_tweet_sentiment(tweet):
    analysis = TextBlob(clean_tweet(tweet))
    if analysis.sentiment.polarity > 0:
        return 'positive'
    elif analysis.sentiment.polarity == 0:
        return 'neutral'
    else:
        return 'negative'


def get_tweets(query, count=10):
    consumer_key = '8960pswi0ALmad8bD27Bofh22'
    consumer_secret = 'hSFcDZUsfwSbn3eutUirambdqLK1dwMyZkL40BAuoYY4mcbLbE'
    access_token = '934833577803616257-mVf5WjNVNfT2eWmQ4T46N2T2BDFZ1tV'
    access_token_secret = '5xQVESFc6kGaQSbtdhvew1WPi73Yne1a9lTi62oPrkKba'

    try:
        auth = OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        api = tweepy.API(auth)
    except:
        print("Error: Authentication Failed")

    tweets = []
    try:
        fetched_tweets = api.search(q=query, count=count)
        for tweet in fetched_tweets:
            parsed_tweet = {}
            parsed_tweet['text'] = tweet.text
            parsed_tweet['sentiment'] = get_tweet_sentiment(tweet.text)

            if tweet.retweet_count > 0:
                if parsed_tweet not in tweets:
                    tweets.append(parsed_tweet)
            else:
                tweets.append(parsed_tweet)
        return tweets
    except tweepy.TweepError as e:
        print("Error : " + str(e))


def supreme(s):
    consumer_key = '8960pswi0ALmad8bD27Bofh22'
    consumer_secret = 'hSFcDZUsfwSbn3eutUirambdqLK1dwMyZkL40BAuoYY4mcbLbE'
    access_token = '934833577803616257-mVf5WjNVNfT2eWmQ4T46N2T2BDFZ1tV'
    access_token_secret = '5xQVESFc6kGaQSbtdhvew1WPi73Yne1a9lTi62oPrkKba'

    try:
        auth = OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        api = tweepy.API(auth)
    except:
        print("Error: Authentication Failed")


    tweets = get_tweets(query=s, count=200)

    ptweets = [tweet for tweet in tweets if tweet['sentiment'] == 'positive']
    ppos = 100 * len(ptweets) / len(tweets)
    # print("Positive tweets percentage: {} %".format(ppos))

    ntweets = [tweet for tweet in tweets if tweet['sentiment'] == 'negative']
    pneg = 100 * len(ntweets) / len(tweets)
    # print("Negative tweets percentage: {} %".format(pneg))

    pneu = (len(tweets) - len(ntweets) - len(ptweets)) / len(tweets)
    neutweets = [tweet for tweet in tweets if tweet['sentiment'] == 'neutral']
    # print("Neutral tweets percentage: {} % \ ".format(100 * (pneu)))

    """
    print("\n\nPositive tweets:")
    for tweet in ptweets[:10]:
        print(tweet['text'])

    print("\n\nNegative tweets:")
    for tweet in ntweets[:10]:
        print(tweet['text'])
    print("\n\nNeutral tweets:")
    for tweet in neutweets[:10]:
        print(tweet['text'])
    """
    return ptweets[:10], ppos, ntweets[:10], pneg, neutweets[:10], pneu
    # return ppos, pneg, pneu


def getTrends():
    pytrends = TrendReq(hl='en-US', tz=360)
    d = pytrends.trending_searches().values
    l = []
    for i in range(len(d)):
        l.append(d[i][0])
    return l[:10]


def getAnalysis(ck="", cs="", at="", ats=""):
    consumer_key = ck
    consumer_secret = cs
    access_token = at
    access_token_secret = ats
    try:
        auth = OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        api = tweepy.API(auth, wait_on_rate_limit=True)
    except:
        print("Error: Authentication Failed")
    topTrends = getTrends()
    analysis = supreme(topTrends[0])
    d = {'positive tweets': analysis[0], 'pp': analysis[1], 'negative tweets': analysis[2],
         'np': analysis[3], 'neutral tweets': analysis[4], 'neup': analysis[5]}
    return d


if __name__ == '__main__':
    consumer_key = '8960pswi0ALmad8bD27Bofh22'
    consumer_secret = 'hSFcDZUsfwSbn3eutUirambdqLK1dwMyZkL40BAuoYY4mcbLbE'
    access_token = '934833577803616257-mVf5WjNVNfT2eWmQ4T46N2T2BDFZ1tV'
    access_token_secret = '5xQVESFc6kGaQSbtdhvew1WPi73Yne1a9lTi62oPrkKba'

    try:
        auth = OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        api = tweepy.API(auth)
    except:
        print("Error: Authentication Failed")

    topTrends = getTrends()
    analysis = supreme(topTrends[0])
    d = {'positive tweets': analysis[0], 'pp': analysis[1], 'negative tweets': analysis[2],
         'np': analysis[3], 'neutral tweets': analysis[4], 'neup': analysis[5]}
    print(d)

#    print(supreme(topTrends[0]))
