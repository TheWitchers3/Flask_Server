import re
import tweepy
from tweepy import OAuthHandler
from textblob import TextBlob



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


def get_tweets(query, count = "10",ck="",cs="",at="",ats=""):
    #Enter your credentials
    consumer_key = ck
    consumer_secret = cs
    access_token = at
    access_token_secret =ats
    try:
        auth = OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        api = tweepy.API(auth,wait_on_rate_limit=True)
    except:
        print("Error: Authentication Failed")
    tweets = []
    try:
        fetched_tweets = api.search(q = query, count = count)

        for tweet in fetched_tweets:
            parsed_tweet = {}
            if tweet.lang == "en":
                parsed_tweet['text'] = clean_tweet(tweet.text)
                parsed_tweet['sentiment'] = get_tweet_sentiment(tweet.text)

            if tweet.retweet_count > 0:
                if parsed_tweet not in tweets:
                    tweets.append(parsed_tweet)
            else:
                tweets.append(parsed_tweet)
        return tweets

    except tweepy.TweepError as e:
        print("Error : " + str(e))


def getAnalysis(query,count,ck,cs,at,ats):
    if(query=="" or count=="" or ck == "" or cs == "" or at=="" or ats == ""):
        return None
    ftweets = get_tweets(query,count,ck,cs,at,ats)
    tweets=[t for t in ftweets if t]
    ptweets = [tweet for tweet in tweets if tweet['sentiment'] == 'positive']

    ptpercentage=100*len(ptweets)/len(tweets)

    ntweets = [tweet for tweet in tweets if tweet['sentiment'] == 'negative']

    ntpercentage = 100 * len(ntweets) / len(tweets)
        
    neutpercentage = 100 * ((len(tweets) - len(ntweets) - len(ptweets)) / len(tweets))
        
    analysis = {}
    analysis['ptweets'] = ptweets
    analysis['ntweets'] = ntweets
    analysis['ptpercentage'] = ptpercentage
    analysis['ntpercentage'] = ntpercentage
    analysis['neutpercentage'] = neutpercentage 
    return analysis

if __name__ == "__main__":
    ana = getAnalysis("modi","20",ck="",cs="",at="",ats="")
    print(ana)
