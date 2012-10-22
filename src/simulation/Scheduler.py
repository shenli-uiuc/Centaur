from Server import Server
from UserNode import UserNode
from Timer import Timer
from TweetGen import TweetGen

class Scheduler:
    timer = None
    tweetGen = None
    server = None
    userNodes = None

    isDone = False

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
        
        self.isDone = self.tweetGen.is_done()

        while self.tweetGen.has_next():
            tweet = self.tweetGen.next()
            print tweet
            self.server.put_to_in_buf(tweet[1], tweet[2])

        self.server.receive()
        self.server.send()
        for user in self.userNodes:
            user.receive()
        
        for user in self.userNodes:
            user.send()

        for user in self.userNodes:
            self.isDone = self.isDone and user.is_done()
            if not self.isDone:
                break

    def simulate(self):
        while not self.isDone:
            self._one_second()
            self.timer.inc_time()

        self.tweetGen.close()

    def test(self):
        for i in range(10):
            self._one_second()
            self.timer.inc_time()

        self.tweetGen.close()

def main():
    scheduler = Scheduler()
    scheduler.test()

if __name__=="__main__":
    main()
