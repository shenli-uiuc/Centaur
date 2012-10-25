import rbtree

class MsgCounter:
    MAX_QUEUE_LEN = 20
    timer = None
    msgQueue = None

    def __init__(self, timer):
        self.timer = timer
        self.msgQueue = rbtree.rbtree()

    def report_receive(self, msgID):
        if not self.msgQueue.has_key(msgID):
            self.msgQueue[msgID] = None
            return True
        return False

    def remove_deprecated(self):
        delta = len(self.msgQueue) - self.MAX_QUEUE_LEN
        if delta > 0:
            i = delta
            while i > 0:
                self.msgQueue.pop()
                i -= 1
