import math

#from Server import Server
from ServerRand import Server
from UserNode import UserNode
from Timer import Timer
from TweetGen import TweetGen
from MyQueue import PQueue

class Scheduler:
    ONE_MINUTE = 60
    EXP_LEN = 120 # in minutes
    INFTY = 9999999

    userNetLogFileName = "rand_user_net.log"
    logFileName = "rand_all.log"

    timer = None
    tweetGen = None
    server = None
    userNodes = None
    userNodeNum = 0

    isDone = False

    userCurNetIn = None
    userCurNetOut = None
    userAccNetIn = None
    userAccNetOut = None

    serverCurNetIn = 0
    serverCurNetOut = 0
    serverSbCurNetOut = 0

    msgID = 0

    msgRecCnt = 0
    msgRecExpCnt = 0
    msgPrevRecCnt = 0
    msgPrevRecExpCnt = 0

    def __init__(self):
        self.timer = Timer()
        self.tweetGen = TweetGen(self.timer)
        self.server = Server(self.timer)
        self.userNodes = self.server.get_user_nodes()
        self.userNodeNum = len(self.userNodes)

        self.userCurNetIn = [0] * self.userNodeNum
        self.userCurNetOut = [0] * self.userNodeNum
        self.userAccNetIn = [0] * self.userNodeNum
        self.userAccNetOut = [0] * self.userNodeNum


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
            self.server.put_to_in_buf(tweet[0], self.msgID, tweet[1], tweet[2])
            self.msgID += 1

        self.server.receive()
        self.server.send()
        self.msgRecExpCnt += self.server.get_msg_rec_exp_cnt()
        #print self.server.get_cur_net_stat()
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

        for user in self.userNodes:
            self.msgRecCnt += user.get_new_msg_count()

        for user in self.userNodes:
            user.rand_fail()

    def simulate(self):
        cnt = 0
        minCnt = 0
        self.msgRecCnt = 0
        self.msgRecExpCnt = 0
        fLog = open(self.logFileName, "w")

        while not self.isDone:
            if minCnt >= self.EXP_LEN:
                break
            self._one_second()
            self.timer.inc_time()
            sTmpIn, sTmpOut, sSbTmpOut = self.server.get_cur_net_stat() 
            self.serverCurNetIn += sTmpIn
            self.serverCurNetOut += sTmpOut
            self.serverSbCurNetOut += sSbTmpOut
            cnt += 1
            #print cnt
            if cnt >= self.ONE_MINUTE:
                cnt = 0
                minCnt += 1
                print minCnt
               
                #read stat from users
                i = 0
                inS = 0
                inS2 = 0
                outS = 0
                outS2 = 0
                delayMin = self.INFTY
                delayMax = 0
                delayS = 0                
                userCnt = 0
                
                self.log_user_net(self.userCurNetIn, self.userCurNetOut)
                
                while i < self.userNodeNum:
                    #first translate the network stat into KB, otherwise it is too large
                    self.userCurNetIn[i] = self.userCurNetIn[i] / 1000.0
                    self.userCurNetOut[i] = self.userCurNetOut[i] / 1000.0
                    self.userAccNetIn[i] += self.userCurNetIn[i]
                    self.userAccNetOut[i] += self.userCurNetOut[i]
                    inS += self.userCurNetIn[i]
                    inS2 += (self.userCurNetIn[i] ** 2)
                    outS += self.userCurNetOut[i]
                    outS2 += (self.userCurNetOut[i] ** 2)

                    delay = self.userNodes[i].get_delay()
                    if delay:
                        delayMin = min(delayMin, delay)
                        delayMax = max(delayMax, delay)
                        delayS += delay 
                        userCnt += 1

                    i += 1
                
                #stat user traffic
                inVar = math.sqrt((inS2 - (inS ** 2 ) / self.userNodeNum) / self.userNodeNum)
                outVar = math.sqrt((outS2 - (outS ** 2) / self.userNodeNum) / self.userNodeNum)
                print ("user traffic", inS / self.userNodeNum, outS / self.userNodeNum, inVar, outVar)
                fLog.write("%f, %f, %f, %f, "%(inS / self.userNodeNum, outS / self.userNodeNum, inVar, outVar))                

                #stat user delay
                print ("delay", delayMin, delayMax, delayS / userCnt)
                fLog.write("%f, %f, %f, "%(delayMin, delayMax, delayS / userCnt));

                #stat server net
                print ("net", self.serverCurNetIn / self.ONE_MINUTE, self.serverCurNetOut / self.ONE_MINUTE, self.serverSbCurNetOut / self.ONE_MINUTE)
                fLog.write("%f, %f, %f, "%(self.serverCurNetIn / self.ONE_MINUTE, self.serverCurNetOut / self.ONE_MINUTE, self.serverSbCurNetOut / self.ONE_MINUTE))
                self.serverCurNetIn = 0
                self.serverCurNetOut = 0
                self.serverSbCurNetOut = 0

                #msg missing rate
                print ("missing", self.msgRecCnt, self.msgRecExpCnt)
                fLog.write("%f, %f\n"%(self.msgRecCnt, self.msgRecExpCnt))
                #maybe I don't need to keep the prev status
                self.msgPrevRecCnt = self.msgRecCnt
                self.msgPrevRecExpCnt = self.msgRecExpCnt

        fLog.close()
        self.tweetGen.close()
        f = open(self.userNetLogFileName, 'w')
        i = 0
        while i < self.userNodeNum:
            f.write("%f,%f\n"%(self.userAccNetIn[i], self.userAccNetOut[i]))
            i += 1
        f.close()

    def log_user_net(self, userNetIn, userNetOut):
        pass

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
