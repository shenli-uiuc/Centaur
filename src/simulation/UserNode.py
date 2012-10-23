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

    #userNetStat
    curNetIn = 0
    curNetOut = 0

    #msgDelayStat
    DELAY_SLOT_NUM = 10
    delayIndex = 0
    delayRoll = None

    def __init__(self, netIn, netOut, pFail, sharedStat, id, x, y):
        self.inBuf = PQueue()
        self.outBuf = FQueue() 
        self.isWorking = True 
        self.delayRoll = [0] * self.DELAY_SLOT_NUM

        self.netIn = netIn
        self.netOut = netOut
        self.pFail = pFail
        self.userNodes = sharedStat['userNodes']
        self.timer = sharedStat['timer']
        self.id = id
        self.x = x
        self.y = y

    def report_delay(self, delay):
        self.delayRoll[self.delayIndex] = delay
        self.delayIndex = (self.delayIndex + 1) % self.DELAY_SLOT_NUM

    def get_delay(self):
        return sum(self.delayIndex) / self.DELAY_SLOT_NUM 

    def receive(self):
        """
        0. inc accIn budget
        1. read from inBuf (consider both cpu and network constraints)
        2. append subtrees to the outBuf
        """
        self.accIn += self.netIn
        self.curNetIn = 0        

        data = self.get_from_in_buf()
        while data:
            timestamp, u, msgLen = data
            self.report_delay(timestamp - self.timer.cur_time())
            #v is the reference to the Vertex object in the DHTree
            for v in u.cList:
                self.put_to_out_buf(timestamp, v, msgLen) 
            data = self.get_from_in_buf()

    def send(self):
        """
        0. inc accOut budget
        1. read from outBuf (consider both cpu and network constraints)
        2. append to receivers' inBuf
        """
        self.accOut += self.netOut
        self.curNetOut = 0

        data = self.get_from_out_buf()
        while data:
            timestamp, u, msgLen = data
            #Arr... there is some redundancy here, both self.userNodes[u.id].x and u.x refers to the same thing
            x1 = self.userNodes[u.id].x
            y1 = self.userNodes[u.id].y
            delay = Util.delay(self.x, self.y, x1, y1)
            #ASSERTION: cur_time() should be in seconds (float)
            self.userNodes[u.id].put_to_in_buf(self.timer.cur_time() + delay, timestamp, u, msgLen) 
            data = self.get_from_out_buf()
            

    #should be called by function receive
    def get_from_in_buf(self):
        """
        get one package from the inBuf if both cpu and network contraints allows
        """
        data = self.inBuf.peek()
        if not data:
            return None
        #the data should be (subtree, msg) pair
        delay, (timestamp, u, msgLen) = data
        size = u.subTreeSize * 8 + msgLen
        if self.timer.cur_time() > delay and size <= self.accIn:
            self.accIn -= size
            self.curNetIn += size
            self.inBuf.pop()
            return (timestamp, u, msgLen)
        else:
            return None

    #should be called by function send of other nodes
    def put_to_in_buf(self, delay, timestamp, subtree, msgLen):
        """
        put one package to the inBuf
        """
        self.inBuf.push(delay, (timestamp, subtree, msgLen))

    #should be called by function receive
    def put_to_out_buf(self, timestamp, subtree, msgLen):
        self.outBuf.push((timestamp, subtree, msgLen))

    #should be called by function send
    def get_from_out_buf(self):
        data = self.outBuf.peek()
        if not data:
            return None
        timestamp, u, msgLen = data
        size = u.subTreeSize + msgLen
        if size <= self.accOut:
            self.accOut -= size
            self.curNetOut += size
            self.outBuf.pop()
            return (timestamp, u, msgLen)
        else:
            return None

    def is_done(self):
        if self.inBuf.is_empty() and self.outBuf.is_empty():
            return True
        else:
            return False

    def rand_fail(self):
        """
        1. when failed drop all msgs in both inBuf and outBuf
        """
        if random.random() < self.pFail:
            self.inBuf.clear()
            self.outBuf.clear()   

    def get_cur_net_stat(self):
        return (self.curNetIn, self.curNetOut) 
