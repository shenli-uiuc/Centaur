import math
import random

from MyQueue import FQueue, PQueue
from UserNode import UserNode
import Util
from DHTree import DHTree
from Timer import Timer

class Server:
   
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

    liveProb = 0.05

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

    coor_file = "../../data/vcoors"

    sharedStat = None
    timer = None

    #accumulated net resources
    accIn = 0
    accOut = 0

    def __init__(self, timer):
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
            user = UserNode(self.userNetIn, self.userNetOut, self.userPFail, self.sharedStat, cnt, longitude, latitude)
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
        data = self.get_from_in_buf()
        while data:
            folNum, msgLen = data
            folNum = math.ceil(self.liveProb * folNum)
            #we do not need to count the incoming traffic, as it gonna be the same with or without Centuar
            folSet = self._get_followers(folNum)
            folSet.insert(0, [self.id, self.x, self.y])
            tree = DHTree(folSet)
            r = tree.get_tree(self.userAngle, self.angle, self.d, self.h)
            for u in r.cList:
                self.put_to_out_buf(u, msgLen)
            data = self.get_from_in_buf()
 
    
    def send(self):
        """
        1. consider the network constraints and send out the msgs
        2. for each tweet, construct the follower set
        3. generate the multicasting tree
        4. do the redundency
        """
        self.accOut += self.netOut
        data = self.get_from_out_buf()
        while data:
            u, msgLen = data
            x1 = self.userNodes[u.id].x
            y1 = self.userNodes[u.id].y
            delay = Util.delay(self.x, self.y, x1, y1)
            sefl.userNodes[u.id].put_to_in_buf(self.timer.cur_time() + delay, u, msgLen)
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
        folNum, msgLen = data
        if msgLen > self.accIn:
            return None
        else:
            self.accIn -= msgLen
            return self.inBuf.pop()

    #folNum is used to determin the number of subscribers for this msg
    def put_to_in_buf(self, folNum, msgLen):
        self.inBuf.push((folNum, msgLen)) 

    def get_from_out_buf(self):
        data = self.outBuf.peek()
        if not data:
            #outBuf is empty
            return None
        u, msgLen = data
        size = u.subTreeSize + msgLen
        if size < self.accOut:
            return None
        else:
            self.accOut -= size 
            return self.outBuf.pop()

    def put_to_out_buf(self, u, msgLen):
        self.outBuf.push((u,msgLen))

    def _get_followers(self, num):
        #given the number of living followers, randomly generate the online follower set 
        folSet = []
        while num > 0:
            id = random.randint(0, self.userNum - 1)
            folSet.append([id, self.userNodes[id].x, self.userNodes[id].y])
            num -=1 
        return folSet

    

def main():
    timer = Timer()
    server = Server(timer)

if __name__ == "__main__":
    main()
     
