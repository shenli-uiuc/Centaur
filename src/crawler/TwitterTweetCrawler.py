from MySQLDataStore import MySQLDataStore
from URLHandler import URLHandler
import time
try:
    import json
except ImportError,e:
    import simplejson as json
import sys



class TwitterTweetCrawler:

    BAD_CHAR_SET = ['\n']

    MAX_TWEET_ID = (2 ** 63) - 1
    tweetCount = 200
    urlGetTweet = "https://api.twitter.com/1/statuses/user_timeline.json?user_id=%d&max_id=%d&count=%d"
    urlHandler = None
    mySQLDataStore = None

    def __init__(self):
        self.urlHandler = URLHandler()
        self.mySQLDataStore = MySQLDataStore()

    def get_tweet_piece(self, userID, maxID):
        print ("get_tweet_piece", userID, maxID) 
        url = self.urlGetTweet%(userID, maxID, self.tweetCount)
        print url
        res = self.urlHandler.open_url(url)
        data = res.read()
        try:
            tweets = json.loads(data)
        except ValueError, e:
            print e.message 
            print data
            sys.exit(0)
        print len(tweets)
        maxID = self.MAX_TWEET_ID
        for tweet in tweets:
            tweetID = tweet['id']
            maxID = min(tweetID, maxID)
            createdAt = tweet['created_at']
            text = tweet['text']
            retweetCount = tweet['retweet_count']
            retweeted = tweet['retweeted']
            pullAt = time.time()
            #print (tweetID, userID, createdAt, text, retweetCount, retweeted, pullAt)
            self.mySQLDataStore.insert_tweet(tweetID, userID, createdAt, text, retweetCount, retweeted, pullAt)
        if maxID >= self.MAX_TWEET_ID:
            return 0
        return maxID

    def get_all_tweets(self, screenName):
        userID = self.mySQLDataStore.get_one_id(screenName)
        if not userID:
            return
        minID = self.mySQLDataStore.select_min_tweet(userID) - 1
        print ("get_all_tweets: ", screenName, userID)
        while minID > 1:
            minID = self.get_tweet_piece(userID, minID) - 1
            print (userID, screenName, minID)
        if minID >= -1:
            self.mySQLDataStore.insert_tweet(-userID, userID, 0, '', 0, False, time.time())


def main():
    tweetCrawler = TwitterTweetCrawler()
    f = open('sample.txt', 'r')
    for line in f:
        screenName = line.split('\n')[0]
        tweetCrawler.get_all_tweets(screenName)
    f.close()

if __name__=='__main__':
    main()
