from MyQueue import PQueue, FQueue
import Util
import random

class UserNode:

    #corresponds to the ID in the DH tree (in the real system, an IP address or P2P ID is also required.)
    id = -1
    #pointer to the array of all user nodes
    userNodes = None
    timer = None
    #incoming network bandwidth
    netIn = 0

    #outgoing network bandwidth
    netOut = 0

    #node failing rate
    pFail = 0

    #coordination
    x = 0
    y = 0

    #an array of receiving packets: priority queue with delay as weight, be careful when maintaining the timestamps
    inBuf = None
    #an array of sending packets: FIFO
    outBuf = None
    
    #accumulated incoming network resources: the user receives the packet only when the accumulated incoming resource is larger than the size of the packet
    accIn = 0
    accOut = 0

    def __init__(self, netIn, netOut, pFail, sharedStat, id, x, y):
        self.inBuf = PQueue()
        self.outBuf = FQueue() 
        self.isWorking = True 

        self.netIn = netIn
        self.netOut = netOut
        self.pFail = pFail
        self.userNodes = sharedStat['userNodes']
        self.timer = sharedStat['timer']
        self.id = id
        self.x = x
        self.y = y

    def receive(self):
        """
        0. inc accIn budget
        1. read from inBuf (consider both cpu and network constraints)
        2. append subtrees to the outBuf
        """
        self.accIn += self.netIn
        
        data = self.get_from_in_buf()
        while data:
            u, msgLen = data
            #v is the reference to the Vertex object in the DHTree
            for v in u.cList:
                put_to_out_buf(v, msgLen) 
            data = self.get_from_in_buf()

    def send(self):
        """
        0. inc accOut budget
        1. read from outBuf (consider both cpu and network constraints)
        2. append to receivers' inBuf
        """
        self.accOut += self.netOut

        data = self.get_from_out_buf()
        while data:
            u, msgLen = data
            #Arr... there is some redundancy here, both self.userNodes[u.id].x and u.x refers to the same thing
            x1 = self.userNodes[u.id].x
            y1 = self.userNodes[u.id].y
            delay = Util.delay(self.x, self.y, x1, y1) 
            #ASSERTION: cur_time() should be in milli-seconds
            self.userNodes[u.id].put_to_in_buf(self.timer.cur_time() + delay, u, msgLen) 
            data = self.get_from_out_buf()
            

    #should be called by function receive
    def get_from_in_buf(self):
        """
        get one package from the inBuf if both cpu and network contraints allows
        """
        #the data should be (subtree, msg) pair
        timestamp, (u, msgLen) = self.inBuf.peek()
        size = u.subTreeSize + msgLen
        if self.timer.cur_time() > timestamp and size <= self.accIn:
            self.accIn -= size
            self.inBuf.pop()
            return (u, msgLen)
        else:
            return None

    #should be called by function send of other nodes
    def put_to_in_buf(self, timestamp, subtree, msgLen):
        """
        put one package to the inBuf
        """
        self.inBuf.push(timestamp, (subtree, msgLen))

    #should be called by function receive
    def put_to_out_buf(self, subtree, msgLen):
        self.outBuf.push((subtree, msgLen))

    #should be called by function send
    def get_from_out_buf(self):
        u, msgLen = self.outBuf.peek()
        size = u.subTreeSize + msgLen
        if size <= self.accOut:
            self.accOut -= size
            self.outBuf.pop()
            return (u, msgLen)
        else:
            return None

    def rand_fail(self):
        """
        1. when failed drop all msgs in both inBuf and outBuf
        """
        if random.random() < self.pFail:
            self.inBuf.clear()
            self.outBuf.clear()    
