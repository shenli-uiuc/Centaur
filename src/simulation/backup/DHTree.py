from NodeGenerator import NodeGenerator
import math

try:
    import json
except ImportError, e:
    import simplejson as json


class DHTree:

    INFTY = 999999999

    d = 0
    h = 0
    alpha = 0
    V = None
    treeSizes = None


    def __init__(self, d, h, alpha, coors):
        self.d = d
        self.h = h
        self.alpha = alpha
        self.V = []
        self.treeSizes = []
        self._init_vertices(coors)
        self._init_tree_sizes()

    def _init_vertices(self, coors):
        cnt = 0
        for coor in coors:
            curV = Vertex(cnt, coor[0], coor[1])
            self.V.append(curV)
            cnt += 1

    def _init_tree_sizes(self):
        for i in range(self.h + 1):
            self.treeSizes.append((self.d ** i - 1) / (self.d - 1))

    def build_tree(self, index, r, curH = 'root'):
        indexLen = len(index)
        r.used = True
        #print (begin, end, r, curH)
        if 'root' == curH:
            curH = self.h
        if curH <= 2 or len(index) <= self.d:
            #print "in curH <= 2"
            for i in range(indexLen):
                if not self.V[index[i]].used:
                    self.V[index[i]].used = True
                    r.cList.append(index[i])
                    self.print_info(r, self.V[index[i]], 0)
            return

        for i in range(indexLen):
            u = self.V[index[i]]
            u.angle = self.get_angle(u.x, u.y, r.x, r.y)

        index.sort(key = lambda i: self.V[i].angle)
        """
        for i in index:
            print (i, self.V[i].x, self.V[i].y, self.V[i].angle)

        exit(0)
        """
        tmpAngle = 0
        cnt = 0
        cv = -1
        cd = self.INFTY
        curIndex = []
        for i in range(indexLen):
            u = self.V[index[i]]
            if u.used and not u == r:
                print "WRONG"
            if u.angle - tmpAngle >= self.alpha or cnt >= self.treeSizes[curH - 1]:
                #if i + 1 >= indexLen and u.angle - tmpAngle < self.alpha and cnt < self.treeSizes[curH-1]:
                #    curIndex.append(index[i])
                if len(curIndex):
                    r.cList.append(cv)
                    self.print_info(r, self.V[cv], cd)
                    self.build_tree(curIndex,  self.V[cv], curH - 1)
                    cnt = 0
                    curIndex = []
                cd = self.INFTY
                cv = -1
                tmpAngle = u.angle


            if not u.used:
                curIndex.append(index[i])
                tmpD = self.get_dist(u.x, u.y, r.x, r.y)
                if tmpD < cd:
                    cd = tmpD
                    cv = index[i]
                cnt += 1

            if i + 1 >= indexLen and u.used:
                print "WRONG!!"
                
            if i + 1 >= indexLen:
                r.cList.append(cv)
                self.print_info(r, self.V[cv], cd)
                self.build_tree(curIndex, self.V[cv], curH - 1)
                break

    def print_info(self, a, b, cd):
        print "%d(%f, %f) connects %d(%f, %f), at distance %f(%f), angle"%(a.id, a.x, a.y, b.id, b.x, b.y, cd, b.angle)

    def _comp(a, b):
        return self.V[a].angle < self.V[b].angle


    def get_dist(self, x1, y1, x2, y2):
        return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

    #non-root node comes first
    def get_angle(self, x1, y1, x2, y2):
        if y1 == y2:
            if x1 > x2:
                return math.pi / 2
            elif x1 < x2:
                return math.pi * (3/2)
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
                f.write("%d %d\n"%(v.id, c))
        f.close()

    def get_tree(self):
        pass

class Vertex:
    id = 0
    x = 0
    y = 0
    angle = 0
    cList = []
    used = False

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
            print '%d %d'%(self.id, i)

def main():
    nodeGenerator = NodeGenerator()
    coors = nodeGenerator.gen(10, 100) 
    tree = DHTree(2, 7, math.pi / 3, coors)
    index = range(len(coors))
    tree.build_tree(index, r = tree.V[0])
    tree.print_tree()
    tree.store_vertices('vertices')
    tree.store_edges('edges')

if __name__ == "__main__":
    main()
