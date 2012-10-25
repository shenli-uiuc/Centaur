from DHTree import Vertex
from NodeGenerator import NodeGenerator

import random

class RandTree:

    d = 0
    h = 0

    V = None
    treeSizes = None

    def __init__(self, coors):
        self.V = []
        self.treeSizes = []
        self._init_vertices(coors)

    def _init_vertices(self, coors):
        for coor in coors:
            curV = Vertex(coor[0], coor[1], coor[2])
            self.V.append(curV)

    def _init_tree_sizes(self):
        for i in range(self.h + 1):
            self.treeSizes.append((self.d ** i - 1) / (self.d - 1))

    def get_tree(self, d, h):
        self.d = d
        self.h = h
        self._init_tree_sizes()
        index = range(len(self.V))
        self.build_tree(index[1:], self.V[0], self.h)
        return self.V[0] 
 
    def build_tree(self, index, r, curH):
        #print (len(index), self.treeSizes[curH - 1])
        if curH < self.h and len(index) < self.d:
            for ind in index:
                r.cList.append(self.V[ind])
            return

        #print "****************"
        indexLen = len(index)
        size = self.treeSizes[curH - 1]
        start = 0
        end = min(size, indexLen)
        while start < indexLen:
            # indexing is not right
            rIndex = random.randint(start, end - 1)
            curInd = index[rIndex]
            index[rIndex] = index[start]
            index[start] = curInd
            r.cList.append(self.V[index[start]])
            if end > start + 1:
                self.build_tree(index[(start + 1):end], self.V[index[start]], curH - 1)
            start = end
            end = min(end + size, indexLen)
    
    def print_nodes(self):
        cnt = 0
        for node in self.V:
            if len(node.cList) > 0:
                for v in node.cList:
                    print v.id,
                print          
                cnt += len(node.cList)
        print cnt

def main():
    nodeGen = NodeGenerator()
    coors = nodeGen.gen(100, 500) 
    tree = RandTree(coors)
    tree.get_tree(2, 5)             
    tree.print_nodes()

if __name__=="__main__":
    main() 
