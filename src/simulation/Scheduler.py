from Server import Server
from UserNode import UserNode
from Timer import Timer
from TweetGen import TweetGen

class Scheduler:
    ONE_MINITE = 60

    timer = None
    tweetGen = None
    server = None
    userNodes = None
    userNodeNum = 0

    isDone = False

    userCurNetIn = None
    userCurNetOut = None

    def __init__(self):
        self.timer = Timer()
        self.tweetGen = TweetGen(self.timer)
        self.server = Server(self.timer)
        self.userNodes = self.server.get_user_nodes()
        self.userNodeNum = len(self.userNodes)

        self.userCurNetIn = [0] * self.userNodeNum
        self.userCurNetOut = [0] * self.userNodeNum

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
            #print tweet
            #timestamp, folNum, msgLen
            self.server.put_to_in_buf(tweet[0], tweet[1], tweet[2])

        self.server.receive()
        self.server.send()
        print self.server.get_cur_net_stat()
        for user in self.userNodes:
            user.receive()
        
        for user in self.userNodes:
            user.send()

        for user in self.userNodes:
            curNetIn, curNetOut = user.get_cur_net_stat()
            self.userCurNetIn[user.id] += curNetIn
            self.userCurNetOut[user.id] += curNetOut 

        for user in self.userNodes:
            self.isDone = self.isDone and user.is_done()
            if not self.isDone:
                break

    def simulate(self):
        cnt = 0
        while not self.isDone:
            self._one_second()
            self.timer.inc_time()
            cnt += 1
            print cnt
            if cnt >= self.ONE_MINITE:
                cnt = 0
                
                i = 0
                inS = 0
                inS2 = 0
                outS = 0
                outS2 = 0
                while i < self.userNodeNum:
                    #first translate the network stat into KB, otherwise it is too large
                    self.userCurNetIn[i] = self.userCurNetIn[i] / 1000.0
                    self.userCurNetOut[i] = self.userCurNetOut[i] / 1000.0
                    inS += self.userCurNetIn[i]
                    inS2 += (self.userCurNetIn[i] ** 2)
                    outS += self.userCurNetOut[i]
                    outS2 += (self.userCurNetOut[i] ** 2)
                    i += 1
                
                inVar = (inS2 - (inS ** 2 ) / self.userNodeNum) / self.userNodeNum
                outVar = (outS2 - (outS ** 2) / self.userNodeNum) / self.userNodeNum
                print (inVar, outVar)

        self.tweetGen.close()

    def test(self):
        for i in range(10):
            self._one_second()
            self.timer.inc_time()

        self.tweetGen.close()

def main():
    scheduler = Scheduler()
    scheduler.simulate()

if __name__=="__main__":
    main()
