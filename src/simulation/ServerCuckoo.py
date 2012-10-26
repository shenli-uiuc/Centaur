import math
import random

from MyQueue import FQueue, PQueue
from UserNodeCuckoo import UserNode
import Util
from DHTree import DHTree, Vertex
from Timer import Timer

class Server:
    SAMPLE_RATE = 0.5

    P2P_TH = 20
   
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
    d = 4
    h = 5

    userNodes = None
    userNum = 0 
    userIDs = None

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
        print "**"
        self.userIDs = range(self.userNum)
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
            folNum = int(math.ceil(self.liveProb * folNum))
            #we do not need to count the incoming traffic, as it gonna be the same with or without Centuar
            uniq, peerIDs = self._get_follower_ids(folNum)
            senderID = random.randint(0, self.userNum - 1)
            if folNum < self.P2P_TH:
                self.userNodes[senderID].store_msg_peer(msgID, peerIDs)
            else:
                gossipNum = int(math.ceil(math.log(folNum)))
                for peer in peerIDs:
                    self.notify_msg_peer(peer, msgID, peerIDs, gossipNum)

            self.userNodes[senderID].put_to_in_buf(self.timer.cur_time(), timestamp, msgID,  msgLen)

            self.msgRecExpCnt += uniq
            data = self.get_from_in_buf()
 
    

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
            return self.inBuf.pop()

    #folNum is used to determin the number of subscribers for this msg
    def put_to_in_buf(self, timestamp, msgID, folNum, msgLen):
        self.inBuf.push((timestamp, msgID, folNum, msgLen)) 

    def get_msg_rec_exp_cnt(self):
        return self.msgRecExpCnt

    def notify_msg_peer(self, userID, msgID, folSet, size):
        #pick size users form folSet, and send the (msgID, list) to userID
        peerList = random.sample(folSet, size)
        self.userNodes[userID].store_msg_peer(msgID, peerList) 

    def _get_follower_ids(self, num):
        if num < self.userNum:
            return (num, random.sample(self.userIDs, num))
        folSet = []
        uniqueSet = set()
        while num > 0:
            id = random.randint(0, self.userNum - 1)
            uniqueSet.add(id)
            folSet.append(id)
            num -= 1
        return (len(uniqueSet), folSet)

    

def main():
    timer = Timer()
    server = Server(timer)

if __name__ == "__main__":
    main()
     
