from MySQLDataStore import MySQLDataStore
from RateLimit import RateLimit
from URLHandler import URLHandler


class TwitterTweetCrawler:

    tweetCount = 200
    urlGetTweet = "https://api.twitter.com/1/statuses/user_timeline.json?screen_name=%s&count=%d&max_id=%d"

    def craw
