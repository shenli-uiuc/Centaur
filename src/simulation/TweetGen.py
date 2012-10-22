"""
tweet format: timestamp, followers_count, msgLen
"""
class TweetGen:
    tweetFilePath = "../../data/shrinked"
    timer = None
    tweetFile = None

    nextTweet = None

    def __init__(self, timer):
        self.timer = timer
        self.tweetFile = open(tweetFilePath, 'r')

    def next(self):
        if not self.has_next():
            return None
        else:
            tweet = self.nextTweet
            self.nextTweet = None
            return tweet

    def has_next(self):
        if not self.nextTweet:
            line = self.tweetFile.readline()
            items.split(',')
            timestamp = int(items[0])
            folNum = int(items[1])
            msgLen = int(items[2]) 
            self.nextTweet = (timestamp, folNum, msgLen)

        if self.nextTweet[0] > self.timer.cur_time():
            return False
        else:
            return True

    def close(self):
        if self.tweetFile.close()
            self.tweetFile.close()
