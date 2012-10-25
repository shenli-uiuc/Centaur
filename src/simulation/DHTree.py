from NodeGenerator import NodeGenerator
import math
import random

try:
    import json
except ImportError, e:
    import simplejson as json

#TODO: give Vertex a real id, rather than a count
class DHTree:

    INFTY = 999999999

    d = 0
    h = 0
    #alpha is the partition angle used by users
    alpha = 0
    #beta is the partition angle used by server. As for some publisher, the online follower set is very mall, the server might need a large angle to take advantage of multicasting.
    beta = 0;
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


    def get_tree(self, alpha, beta, d, h):
        self.d = d
        self.h = h
        self.alpha = alpha
        self.beta = beta
        index = range(1, len(self.V))
        self._init_tree_sizes()
        self.build_tree(index, self.V[0], self.h) 
        return self.V[0]

    def build_tree(self, index, r, curH):
        #print (r.id, index)
        r.used = True
        indexLen = len(index)  
        r.subTreeSize = indexLen      

        #we are not enforcing the DHTree to stay lower than self.h by using the curH parameter (the previous implementation still uses curH parameter because there might be used nodes in the index list)
        #print ("see tree size:", indexLen, curH, self.treeSizes[curH-1])
        """
        The first condition guarantees that even if the number of receivers is small, the data center will also take advantage of the multicasting
        """
        if (not curH == self.h) and len(index) <= self.d: 
            for i in range(indexLen):
                #in the sorting phase, we should enforce that all nodes in the index array are un-used
                if self.V[index[i]].used:
                    print "WRONG: why used!?"
                self.V[index[i]].used = True
                r.cList.append(self.V[index[i]])
                #self.print_info(r, self.V[index[i]], 0)
            return

        if curH == self.h:
            #we are doing with root (DC), hence we can have much more children here. Actually, the number of children of the DC should be calculated with curH
            alpha = self.beta
        else:
            alpha = self.alpha

        for i in range(indexLen):
            u = self.V[index[i]]
            u.angle = self.get_angle(u.x, u.y, r.x, r.y)

        index.sort(key = lambda i: self.V[i].angle)


        tmpAngle = 0
        curIndex = []
        cvi = -1
        cnt = 0
        cd = self.INFTY
        for i in range(indexLen):
            u = self.V[index[i]]
            if u.used:
                print "Wrong2: why used!?"

            #if no nodes in some region, the angle should be skipped
            if 0 >= len(curIndex):
                tmpAngle = u.angle


            """
            The root (DC) choose a random node as children. All other internal nodes choose the nearest node as children.
            in both case we should remember the index in the index array, so that we can do the swap latter 
            """
            if u.angle-tmpAngle > alpha or cnt > self.treeSizes[curH - 1]:
                #print (u.angle, tmpAngle, alpha, cnt, self.treeSizes[curH - 1], curH, i, indexLen)
                if curH == self.h:
                    cvi = random.randint(0, len(curIndex) - 1)   

                tmp = curIndex[cvi]
                curIndex[cvi] = curIndex[0]
                curIndex[0] = tmp

                r.cList.append(self.V[curIndex[0]])  #connecting the tree
                if len(curIndex) > 1:
                    self.build_tree(curIndex[1:], self.V[curIndex[0]], curH - 1)        
                else:
                    self.V[curIndex[0]].used = True 
                cnt = 0
                curIndex = []
                cvi = -1
                tmpAngle = u.angle
                cd = self.INFTY

            curIndex.append(index[i])
            tmpD = self.get_dist(u.x, u.y, r.x, r.y)
            if tmpD < cd:
                cd = tmpD
                cvi = cnt #index in the curIndex array
            cnt += 1

            if i + 1 >= indexLen:
                if curH == self.h:
                    cvi = random.randint(0, len(curIndex) - 1)

                tmp = curIndex[cvi]
                curIndex[cvi] = curIndex[0]
                curIndex[0] = tmp

                r.cList.append(self.V[curIndex[0]])  #connecting the tree
                if len(curIndex) > 1:
                    self.build_tree(curIndex[1:], self.V[curIndex[0]], curH - 1)
                else:
                    self.V[curIndex[0]].used = True

            """
            curIndex.append(index[i])
            tmpD = self.get_dist(u.x, u.y, r.x, r.y)
            if tmpD < cd:
                cd = tmpD
                cvi = cnt #index in the curIndex array
            """


    def print_info(self, a, b, cd):
        print "%d(%f, %f) connects %d(%f, %f), at distance %f(%f), angle"%(a.id, a.x, a.y, b.id, b.x, b.y, cd, b.angle)

    def _comp(a, b):
        return self.V[a].angle < self.V[b].angle


    def get_dist(self, x1, y1, x2, y2):
        return math.sqrt((x1 - float(x2)) ** 2 + (y1 - float(y2)) ** 2)

    #non-root node comes first
    def get_angle(self, x1, y1, x2, y2):
        if y1 == y2:
            if x1 > x2:
                return math.pi / 2
            elif x1 < x2:
                return math.pi * (3/2.0)
            else:
                return 0
 
        angle = math.atan((x1 - x2) / float(y1 - y2)) 
        if angle < 0:
            angle += math.pi
        if x1 < x2:
            angle += math.pi
        #print angle

        return angle

    def print_tree(self):
        print len(self.V)
        for v in self.V:
            print v
        #for v in self.V:
        #    v.print_edges()

    def store_vertices(self, filename, append = False):
        if append:
            f = open(filename, 'a')
        else:
            f = open(filename, 'w')
        for v in self.V:
            f.write("%s\n"%(v))
        f.close()

    def store_edges(self, filename, append = False):
        if append:
            f = open(filename, 'a')
        else:
            f = open(filename, 'w')

        for v in self.V:
            for c in v.cList:
                f.write("%d %d\n"%(v.id, c.id))
        f.close()


class Vertex:
    NODE_SIZE_IN_MEM = 20 #the bytes required to keep one node when transmission
    #the id field maps to the global node id, rather the index in V
    id = 0
    x = 0
    y = 0
    angle = 0
    #cList stores the Vertex object instance
    cList = []
    used = False
    subTreeSize = 0

    def __init__(self, id, x, y):
        self.id = id
        self.x = x
        self.y = y
        self.cList = []

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return '%d %f %f %f'%(self.id, self.x, self.y, self.angle)    

    def print_edges(self):
        for i in self.cList:
            print '%d %d'%(self.id, i.id)

def main():
    nodeGenerator = NodeGenerator()
    coors = nodeGenerator.gen(10, 200) 
    tree = DHTree(coors)
    tree.get_tree(math.pi / 3, math.pi / 4, 2, 7)
    tree.print_tree()
    tree.store_vertices('vertices')
    tree.store_edges('edges')

if __name__ == "__main__":
    main()
