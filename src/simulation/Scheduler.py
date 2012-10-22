from Server import Server
from UserNode import UserNode
from Timer import Timer
from TweetGen import TweetGen

class Scheduler:
    timer = None
    tweetGen = None
    server = None
    userNodes = None

    def __init__(self):
        self.timer = Timer()
        self.tweetGen = TweetGen(self.timer)
        self.server = Server(self.timer)
        self.userNodes = self.server.get_user_nodes()

    def _one_second(self):
        """
        1. while tweetGen generate tweet
        2. in while put tweet into server's inBuf
        3. server send
        4. every user receive
        5. every user send 
        """ 

