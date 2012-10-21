from MyQueue import FQueue, PQueue
import random

import UserNode
import Util

class Server:
    
    inBuf = None
    outBuf = None

    #10GB incoming outgoing network bandwidth
    netIn = 10 * 1024 * 1024 * 1024  
    netout = netIn

    #10KB user incoming and outgoing network bandwidh
    userNetIn = 10 * 1024
    userNetOut = userNetIn
    userPFail = 0.05

    userNodes = None
    userNum = 0 

    coor_file = "../../data/coors"

    sharedStat = None
    timer = None

    def __init__(self, timer):
        self.userNodes = []
        self.sharedStat = {}
        self.sharedStat['userNodes'] = self.userNodes
        self.sharedStat['timer'] = self.timer

    def _init_folower_set(self):
        f = open(coor_file, 'r')
        cnt = 0
        for line in f:
            items = line.split(', ')
            latitude = float(items[0])
            longitude = float(items[1])
            user = UserNode(self.userNetIn, self.userNetOut, self.userPFail, self.sharedStat, cnt, longitude, latitude)
            self.userNodes.append(user)
            cnt += 1
        f.close()
        self.userNum = len(self.userNodes)

    #unified interface for the scheduler to call
    def receive(self):
        """
        1. consider the network constraints
        2. read from inBuf, compute the DHTree and put msgs into outBuf
        """
        pass
    
    def send(self):
        """
        1. consider the network constraints and send out the msgs
        2. for each tweet, construct the follower set
        3. generate the multicasting tree
        4. do the redundency
        """
        pass

    """
    inBuf data fields:
    1. follower num
    2. msg len
    """
    def get_from_in_buf(self):
        pass

    #folNum is used to determin the number of subscribers for this msg
    def put_to_in_buf(self, folNum, msg):
        pass

    def get_from_out_buf(self):
        pass

    def put_to_in_buf(self, u, msg):
        pass 

    def _get_followers(self, num):
        #given the number of living followers, randomly generate the online follower set 
        folSet = []
        while num > 0:
            id = random.randint(0, self.userNum - 1)
            folSet.append(id)
            num -=1 
        return folSet

     
