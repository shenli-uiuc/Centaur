from collections import deque
import heapq

class PQueue:
    arr = None

    def __init__(self):
        self.arr = []

    def push(self, pri, d):
        heapq.heappush(self.arr, (pri, d))

    def pop(self):
        pri, d = heapq.heappop(self.arr)
        return d

    def peek(self):
        return self.arr[0]

    def is_empty(self):
        return (len(self.arr) <= 0)

    def clear(self):
        self.arr = []


class FQueue:
    q = None

    def __init__(self):
        self.q = deque()

    def push(self, data):
        self.q.append(data)

    def pop(self):
        return self.q.popleft()

    def peek(self):
        return self.q[0]

    def is_empty(self):
        return len(self.q) <= 0

    def clear(self):
        self.q.clear()

#testing
def main():
    q = FQueue()
    q.push("abc")
    q.push("123")
    q.push("def")
    print q.peek()
    while not q.is_empty():
        print q.pop()
    heap = PQueue()
    heap.push(7, 'c')
    heap.push(3, 'b')
    heap.push(-9, 'a');
    heap.push(10, 'd');
    print heap.peek()

    while(not heap.is_empty()):
        print heap.pop()


if __name__=="__main__":
    main()

