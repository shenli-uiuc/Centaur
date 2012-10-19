from MyQueue import PQueue, FQueue
import Util

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
    isWorking = True
    #TODO: consider the failure

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

    def UserNode(self, netIn, netOut, pFail, sharedStat, id, x, y):
        self.inBuf = PQueue()
        self.outBuf = FQueue() 
        self.isWorking = True 

        self.netIn = netId
        self.netOut = netOut
        self.pFail = pFail
        self.userNodes = sharedStat.userNodes
        self.timer = sharedStat.timer
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
            u, msg = data
            for v in u.cList:
                put_to_out_buf(v, msg) 
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
            u, msg = data
            x1 = self.userNodes[u.id].x
            y1 = self.userNodes[u.id].y
            delay = Util.delay(x, y, x1, y1) 
            #ASSERTION: cur_time() should be in milli-seconds
            self.userNodes[u.id].put_to_in_buf(self.timer.cur_time() + delay, u, msg) 
            data = self.get_from_out_buf()
            

    #should be called by function receive
    def get_from_in_buf(self):
        """
        get one package from the inBuf if both cpu and network contraints allows
        """
        #the data should be (subtree, msg) pair
        timestamp, (u, msg) = self.inBuf.peek()
        size = u.subTreeSize + len(msg)
        if self.timer.cur_time() > timestamp and size <= self.accIn:
            self.accIn -= size
            self.inBuf.pop()
            return (u, msg)
        else:
            return None

    #should be called by function send of other nodes
    def put_to_in_buf(self, timestamp, subtree, msg):
        """
        put one package to the inBuf
        """
        self.inBuf.push(timestamp, (subtree, msg))

    #should be called by function receive
    def put_to_out_buf(self, subtree, msg):
        self.outBuf.push((subtree, msg))

    #should be called by function send
    def get_from_out_buf(self):
        u, msg = self.outBuf.peek()
        size = u.subTreeSize + len(msg)
        if size <= self.accOut:
            self.accOut -= size
            self.outBuf.pop()
            return (u, msg)
        else:
            return None

    def rand_fail(self):
        """
        1. called by scheduler, when called, has a change to switch between failed and working
        2. when failed drop all msgs in both inBuf and outBuf
        """
        pass
