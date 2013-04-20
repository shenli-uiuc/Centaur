from MyQueue import PQueue, FQueue
from MsgCounter import MsgCounter
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
    accNetDelay = 0

    #msgDelayStat
    DELAY_SLOT_NUM = 10
    delayIndex = 0
    delayCnt = 0
    delayRoll = None
    maxDelay = 0

    #msg missing rate stat
    msgCount = None
    newMsgCount = 0

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
        self.msgCount = MsgCounter(self.timer)
        self.id = id
        self.x = x
        self.y = y

    def report_delay(self, delay):
        #self.delayCnt = min(self.delayCnt + 1, self.DELAY_SLOT_NUM)
        #print ("user delay: ", delay)
        #self.delayRoll[self.delayIndex] = delay
        #self.delayIndex = (self.delayIndex + 1) % self.DELAY_SLOT_NUM
        if self.maxDelay < delay:
            self.maxDelay = delay

    def get_delay(self):
        tmpDelay = self.maxDelay
        self.maxDelay = 0
        return tmpDelay

    def receive(self):
        """
        0. inc accIn budget
        1. read from inBuf (consider both cpu and network constraints)
        2. append subtrees to the outBuf
        """
        self.accIn += self.netIn
        self.curNetIn = 0        
        self.accNetDelay = max(0, self.accNetDelay - 1)
        self.newMsgCount = 0

        data = self.get_from_in_buf()
        while data:
            prevDelay, (timestamp, msgID, u, msgLen) = data
            self.report_delay(prevDelay - timestamp)
            if self.msgCount.report_receive(msgID):
                self.newMsgCount += 1
            #v is the reference to the Vertex object in the DHTree
            for v in u.cList:
                self.put_to_out_buf(prevDelay, timestamp, msgID, v, msgLen) 
            data = self.get_from_in_buf()
        self.msgCount.remove_deprecated()

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
            prevDelay, timestamp, msgID, u, msgLen = data
            #Arr... there is some redundancy here, both self.userNodes[u.id].x and u.x refers to the same thing
            x1 = self.userNodes[u.id].x
            y1 = self.userNodes[u.id].y
            delay = Util.delay(self.x, self.y, x1, y1)
            net = Util.net(self.x, self.y, x1, y1)
            delay += ((u.subTreeSize + msgLen ) / net )
            #print ("send delay", delay)
            #print (self.x, self.y, x1, y1, delay)
            #ASSERTION: cur_time() should be in seconds (float)
            self.userNodes[u.id].put_to_in_buf(prevDelay + delay, timestamp, msgID, u, msgLen) 
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
        delay, (timestamp, msgID, u, msgLen) = data
        size = u.subTreeSize * u.NODE_SIZE_IN_MEM + msgLen
        if self.timer.cur_time() > delay and size <= self.accIn:
            self.accIn -= size
            self.curNetIn += size
            self.inBuf.pop()
            return data
        else:
            return None

    #should be called by function send of other nodes
    def put_to_in_buf(self, delay, timestamp, msgID, subtree, msgLen):
        """
        put one package to the inBuf
        """
        self.accNetDelay += (float(subtree.subTreeSize * subtree.NODE_SIZE_IN_MEM  + msgLen ) / self.netIn)
        delay += self.accNetDelay
        self.inBuf.push(delay, (timestamp, msgID, subtree, msgLen))

    #should be called by function receive
    def put_to_out_buf(self, prevDelay, timestamp, msgID, subtree, msgLen):
        self.outBuf.push((prevDelay, timestamp, msgID, subtree, msgLen))

    #should be called by function send
    def get_from_out_buf(self):
        data = self.outBuf.peek()
        if not data:
            return None
        prevDelay, timestamp, msgID, u, msgLen = data
        size = u.subTreeSize * u.NODE_SIZE_IN_MEM + msgLen
        if size <= self.accOut:
            self.accOut -= size
            self.curNetOut += size
            self.outBuf.pop()
            return data
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

    def get_new_msg_count(self):
        return self.newMsgCount
