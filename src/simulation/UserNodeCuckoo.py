from MyQueue import PQueue, FQueue
from MsgCounter import MsgCounter
import Util
import random
import math

import rbtree


class UserNode:

    #corresponds to the ID in the DH tree (in the real system, an IP address or P2P ID is also required.)
    id = -1
    #pointer to the array of all user nodes
    userNodes = None
    p2pHops = 0
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

    #pending msg peer list: the size should be bounded
    msgPeerDict = None
    MSG_PEER_LEN = 200

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

    #msg missing rate stat
    msgCount = None
    newMsgCount = 0

    def __init__(self, netIn, netOut, pFail, sharedStat, id, x, y):
        self.inBuf = PQueue()
        self.outBuf = FQueue() 
        self.isWorking = True 
        self.delayRoll = [0] * self.DELAY_SLOT_NUM

        self.msgPeerDict = rbtree.rbtree()

        self.netIn = netIn
        self.netOut = netOut
        self.pFail = pFail
        self.userNodes = sharedStat['userNodes']
        self.timer = sharedStat['timer']
        self.msgCount = MsgCounter(self.timer)
        self.id = id
        self.x = x
        self.y = y

    def start(self, hops):
        self.p2pHops = hops

    def store_msg_peer(self, msgID, peerList):
        if self.msgPeerDict.has_key(msgID):
            self.msgPeerDict[msgID].extend(peerList)
        else:
            self.msgPeerDict[msgID] = peerList
        if len(self.msgPeerDict) > self.MSG_PEER_LEN:
            self.msgPeerDict.pop()

    def report_delay(self, delay):
        self.delayCnt = min(self.delayCnt + 1, self.DELAY_SLOT_NUM)
        #print ("user delay: ", delay)
        self.delayRoll[self.delayIndex] = delay
        self.delayIndex = (self.delayIndex + 1) % self.DELAY_SLOT_NUM

    def get_delay(self):
        if self.delayCnt <=0:
            return None
        else:
            return (max(self.delayRoll), float(sum(self.delayRoll)) / self.delayCnt)

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
            prevDelay, (timestamp, msgID, msgLen) = data
            self.report_delay(prevDelay - timestamp)
            if self.msgCount.report_receive(msgID):
                self.newMsgCount += 1
            
            #if not has_key, it means that the user has already received the msg before, or the msg is too old in which case, the entry has been deleted
            if self.msgPeerDict.has_key(msgID):
                peerList = self.msgPeerDict[msgID]
                del self.msgPeerDict[msgID] 
                self.put_to_out_buf(prevDelay, timestamp, msgID, peerList, msgLen)
            #else:
            #    print (msgID, "no key" )
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
            prevDelay, timestamp, msgID, peerList, msgLen = data
            #Arr... there is some redundancy here, both self.userNodes[u.id].x and u.x refers to the same thing
            for peerID in peerList:
                x1 = self.userNodes[peerID].x
                y1 = self.userNodes[peerID].y
                delay = self.p2pHops * Util.delay(self.x, self.y, x1, y1)
                net = Util.net(self.x, self.y, x1, y1)
                delay += (msgLen  / net )
                #print prevDelay + delay
                self.userNodes[peerID].put_to_in_buf(prevDelay + delay, timestamp, msgID, msgLen) 
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
        delay, (timestamp, msgID, msgLen) = data
        size = msgLen
        if self.timer.cur_time() > delay and size <= self.accIn:
            self.accIn -= size
            self.curNetIn += size
            self.inBuf.pop()
            return data
        else:
            return None

    #should be called by function send of other nodes
    def put_to_in_buf(self, delay, timestamp, msgID, msgLen):
        """
        put one package to the inBuf
        """
        self.accNetDelay += (float(msgLen ) / self.netIn)
        delay += self.accNetDelay
        self.inBuf.push(delay, (timestamp, msgID, msgLen))

    #should be called by function receive
    def put_to_out_buf(self, prevDelay, timestamp, msgID, peerList, msgLen):
        self.outBuf.push((prevDelay, timestamp, msgID, peerList, msgLen))

    #should be called by function send
    def get_from_out_buf(self):
        data = self.outBuf.peek()
        if not data:
            return None
        prevDelay, timestamp, msgID, peerList, msgLen = data
        size = len(peerList) * msgLen
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
