import math
import random

from MyQueue import FQueue, PQueue
from UserNode import UserNode
import Util
from DHTree import Vertex
from Timer import Timer
from RandTree import RandTree

class Server:
    SAMPLE_RATE = 0.5
   
    id = 0 
    inBuf = None
    outBuf = None

    #twitter office location, well, I don't know where its is...
    latitude = 37.782587
    longitude = -122.400595
    x = 0
    y = 0

    #10GB incoming outgoing network bandwidth
    netIn = 10 * 1024 * 1024 * 1024  
    netOut = netIn

    #keep current server in/out bandwidth
    curNetIn = 0
    curNetOut = 0

    sbNetOut = 0 #server broadcast net out

    liveProb = 0.1

    #10KB user incoming and outgoing network bandwidh
    userNetIn = 10 * 1024
    userNetOut = userNetIn
    userPFail = 0.05

    #for tree partition 
    userAngle = math.pi / 6
    angle = math.pi
    # (d, h) = (4, 5) lead to at most 340 descendant
    d = 2
    h = 8

    userNodes = None
    userNum = 0 

    coor_file = "../../data/small_coors"

    sharedStat = None
    timer = None

    #accumulated net resources
    accIn = 0
    accOut = 0

    #msg missing rate
    msgRecExpCnt = 0
    REDUNDANCY = 3

    def __init__(self, timer):
        self.timer = timer

        self.userNodes = []
        self.sharedStat = {}
        self.sharedStat['userNodes'] = self.userNodes
        self.sharedStat['timer'] = self.timer
        self.x, self.y = Util.loc2coor(self.latitude, self.longitude)

        self.inBuf = FQueue()
        self.outBuf = FQueue()
        self._init_follower_set()

    def _init_follower_set(self):
        f = open(self.coor_file, 'r')
        cnt = 0
        for line in f:

            items = line.split(',')
            latitude = float(items[0])
            longitude = float(items[1])
            x, y = Util.loc2coor(latitude, longitude)
            user = UserNode(self.userNetIn, self.userNetOut, self.userPFail, self.sharedStat, cnt, x, y)
            self.userNodes.append(user)
            cnt += 1
        f.close()
        self.userNum = cnt
        self.id = cnt

    def get_user_nodes(self):
        return self.userNodes        

    #unified interface for the scheduler to call
    def receive(self):
        """
        1. consider the network constraints
        2. read from inBuf, compute the DHTree and put msgs into outBuf
        """
        self.accIn += self.netIn
        self.curNetIn = 0
        self.sbNetOut = 0
        data = self.get_from_in_buf()
        self.msgRecExpCnt = 0
        while data:
            timestamp, msgID, folNum, msgLen = data
            folNum = math.ceil(self.liveProb * folNum)
            #we do not need to count the incoming traffic, as it gonna be the same with or without Centuar
            uniqCnt, folSet = self._get_followers(folNum)
            self.msgRecExpCnt += uniqCnt
            folSet.insert(0, [self.id, self.x, self.y])
            self.sbNetOut += (folNum * (Vertex.NODE_SIZE_IN_MEM + msgLen))
            for i in range(self.REDUNDANCY):
                tree = RandTree(folSet)
                r = tree.get_tree(self.d, self.h)
                for u in r.cList:
                    self.put_to_out_buf(timestamp, msgID, u, msgLen)
            data = self.get_from_in_buf()
 
    
    def send(self):
        """
        1. consider the network constraints and send out the msgs
        2. for each tweet, construct the follower set
        3. generate the multicasting tree
        4. do the redundency
        """
        self.accOut += self.netOut
        self.curNetOut = 0
        data = self.get_from_out_buf()
        while data:
            timestamp, msgID, u, msgLen = data
            x1 = self.userNodes[u.id].x
            y1 = self.userNodes[u.id].y
            delay = Util.delay(self.x, self.y, x1, y1)
            net = Util.net(self.x, self.y, x1, y1)
            delay += ((u.subTreeSize + msgLen ) / net )
            self.userNodes[u.id].put_to_in_buf(self.timer.cur_time() + delay, timestamp, msgID, u, msgLen)
            data = self.get_from_out_buf()

    """
    inBuf data fields:
    1. follower num
    2. msg len
    """
    def get_from_in_buf(self):
        # we consider the msg as the entire json string
        data = self.inBuf.peek()
        if not data:
            #inBuf is empty
            return None
        timestamp, msgID, folNum, msgLen = data
        if msgLen > self.accIn:
            return None
        else:
            self.accIn -= msgLen
            self.curNetIn += msgLen
            return self.inBuf.pop()

    #folNum is used to determin the number of subscribers for this msg
    def put_to_in_buf(self, timestamp, msgID, folNum, msgLen):
        self.inBuf.push((timestamp, msgID, folNum, msgLen)) 

    def get_from_out_buf(self):
        data = self.outBuf.peek()
        if not data:
            #outBuf is empty
            return None
        timestamp, msgID, u, msgLen = data
        #id takes 8 bytes, in real case it might need more: ip, and other info. TODO: see what is required to start an connection
        size = u.subTreeSize * u.NODE_SIZE_IN_MEM + msgLen
        if size > self.accOut:
            return None
        else:
            self.accOut -= size 
            self.curNetOut += size
            return self.outBuf.pop()

    def get_cur_net_stat(self):
        return (self.curNetIn, self.curNetOut, self.sbNetOut)

    def get_msg_rec_exp_cnt(self):
        return self.msgRecExpCnt

    def put_to_out_buf(self, timestamp, msgID, u, msgLen):
        self.outBuf.push((timestamp, msgID, u, msgLen))

    def _get_followers(self, num):
        #given the number of living followers, randomly generate the online follower set 
        folSet = []
        uniqueSet = set()
        while num > 0:
            id = random.randint(0, self.userNum - 1)
            uniqueSet.add(id)
            folSet.append([id, self.userNodes[id].x, self.userNodes[id].y])
            num -=1 
        return (len(uniqueSet), folSet)

    

def main():
    timer = Timer()
    server = Server(timer)

if __name__ == "__main__":
    main()
     
