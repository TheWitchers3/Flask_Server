import random
import re
import nltk
import tweepy
from newsapi import NewsApiClient
from pytrends.request import TrendReq
from rake_nltk import Rake
from textblob import TextBlob
from tweepy import OAuthHandler

nltk.download()
nltk.download('stopwords')
nltk.download('punkt')

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

    ptweets = [tweet for tweet in tweets if tweet['sentiment'] == 'positiv  e']
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

    newsapi = NewsApiClient(api_key='bb0f664df41346a38b42d10e3682c915')

    all_news = newsapi.get_everything(q=s)
    l1 = all_news.get('articles')
    newsl = []
    titles = []
    for i in l1:
        if i.get('content'):
            newsl.append(i.get('content'))
            titles.append(i.get('title').lower())

    r = Rake()

    l1 = []
    for i in newsl:
        r.extract_keywords_from_text(i)
        for j in r.get_ranked_phrases():
            l1.append(j)

    l = []
    if pneg + 0.5 * pneu > 50:
        tweets1 = ntweets[:]
    else:
        tweets1 = tweets[:]
    for i in tweets1:
        l.append(i.get('text'))

    l2 = []
    for i in l:
        r.extract_keywords_from_text(i)
        for j in r.get_ranked_phrases():
            l2.append(j)

    intersection = list(set([value.lower() for value in l1 if value in l2 and len(value) > 2]))
    titleRank = []
    for i in titles:
        titleRank.append(len(set(i.split()) & set(intersection)))

    truthfulness = True if len(intersection) > 2 else False

    return ptweets, ppos, ntweets, pneg, neutweets, pneu, intersection, truthfulness,titles[titleRank.index(max(titleRank))]

    # return ppos, pneg, pneu


def getTrends():
    pytrends = TrendReq(hl='en-US', tz=360)
    return pytrends.trending_searches(pn='india').to_dict()


def getAnalysis(query, ck="", cs="", at="", ats=""):
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
    analysis = supreme(query)
    d = {'positiveTweets': analysis[0], 'pp': analysis[1], 'negativeTweets': analysis[2],
         'np': analysis[3], 'neutralTweets': analysis[4], 'neup': analysis[5], 'intersection': analysis[6],
         'truthfulness': analysis[7], 'title': analysis[8]}
    return d


def getNotifyTrends():
    pytrends = TrendReq(hl='en-US', tz=360)
    d = pytrends.trending_searches(pn='india').to_dict()
    d = d[0]
    ret_dic = {}
    for i in d:
        if i < 10:
            ret_dic[i + 1] = d[i]
    return {'notif': list(ret_dic.values())[random.randint(0, 9)]}


print(supreme('corona'))
