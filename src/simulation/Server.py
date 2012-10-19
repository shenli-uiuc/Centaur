from MyQueue import FQueue, PQueue

class Server:
    
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

    def get_from_in_buf(self):
        pass

    #folNum is used to determin the number of subscribers for this msg
    def put_to_in_buf(self, folNum, msg):
        pass

    def get_from_out_buf(self):
        pass

    def put_to_in_buf(self, u, msg):
        pass 

    def get_followers(self, folNum):
        #given the number of followers, randomly generate the online follower set 
        pass

     
