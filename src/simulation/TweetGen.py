"""
tweet format: timestamp, followers_count, msgLen
"""
class TweetGen:
    tweetFilePath = "../../data/shrinked"
    timer = None
    tweetFile = None

    nextTweet = None
    isDone = False

    def __init__(self, timer):
        self.timer = timer
        self.tweetFile = open(self.tweetFilePath, 'r')

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
            if not line:
                self.isDone = True
                return False
            items = line.split(',')
            timestamp = int(items[0])
            folNum = int(items[1])
            msgLen = int(items[2]) 
            self.nextTweet = (timestamp, folNum, msgLen)

        if self.nextTweet[0] > self.timer.cur_time():
            return False
        else:
            return True

    def is_done(self):
        return self.isDone        

    def close(self):
        if self.tweetFile:
            self.tweetFile.close()
