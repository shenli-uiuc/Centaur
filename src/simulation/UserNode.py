class UserNode:

    #corresponds to the ID in the DH tree (in the real system, an IP address or P2P ID is also required.)
    id = -1
    #pointer to the array of all user nodes
    userNodes = None

    #incoming network bandwidth
    netIn = 0

    #outgoing network bandwidth
    netOut = 0

    #the maximum number of msg one node can process at each round: corresponds to the cpu constraints
    maxMsgProc = 0

    #node failing rate
    pFail = 0

    #coordination
    x = 0
    y = 0

    #an array of receiving packets: priority queue with delay as weight
    inBuf = []
    #an array of sending packets: FIFO
    outBuf = []
    
    #accumulated incoming network resources: the user receives the packet only when the accumulated incoming resource is larger than the size of the packet
    accIn = 0
    accOut = 0

    def UserNode(self, netIn, netOut, pFail, userNodes, id, x, y):
        self.netIn = netId
        self.netOut = netOut
        self.pFail = pFail
        self.userNodes = userNodes
        self.id = id
        self.x = x
        self.y = y

    def receive(self):
        """
        1. read from inBuf (consider both cpu and network constraints)
        2. append subtrees to the outBuf
        """
        pass

    def send(self):
        """
        1. read from outBuf (consider both cpu and network constraints)
        2. append to receivers' inBuf
        """
        pass

    #should be called by function receive
    def get_from_in_buf(self):
        """
        get one package from the inBuf is both cpu and network contraints allows
        """
        pass

    #should be called by function send of other nodes
    def put_to_in_buf(self, subtree, msg, delay):
        """
        put one package to the inBuf
        """
        pass

    #should be called by function receive
    def put_to_out_buf(self, subtree, msg):
        pass

    #should be called by function send
    def get_from_out_buf(self):
        pass

    def rec_from_buf(self):
        pass
    
    def send_to_buf(self):
        #return False means I am done with my current work. The scheduler will use this to tell whether the simultion is over.
        if len(sendBuf) <= 0:
            return False
        delCnt = 0
        for u in sendBuf:
            if u.subTreeSize > accOut:
                return True
            else:
                accOut -= u.subTreeSize
                recID = u.id
                for child in u.cList:
                    self.userNodes[recID].receive(child)
                delCnt += 1

        for i in range(delCnt):
            del sendBuf[0]


    def one_step(self):
        """
        deduct data from the head of recBuf
        """
        accIn += netIn
        accOut += netOut
        self.send()
        
