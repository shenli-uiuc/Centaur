from NodeGenerator import NodeGenerator
import math
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

    def build_tree(self, index, begin, end, r, curH = 'root'):
        r.used = True
        #print (begin, end, r, curH)
        if 'root' == curH:
            curH = self.h
        if curH <= 2:
            #print "in curH <= 2"
            for i in range(begin, end):
                if not self.V[index[i]].used:
                    self.V[index[i]].used = True
                    r.cList.append(index[i])
            return

        for i in range(begin, end):
            u = self.V[index[i]]
            u.angle = self.get_angle(u.x, u.y, r.x, r.y)

        index[begin:end] = sorted(index[begin:end], key = lambda i: self.V[i].angle)
        """
        for i in index:
            print (i, self.V[i].x, self.V[i].y, self.V[i].angle)

        exit(0)
        """
        tmpAngle = 0
        cnt = 0
        cv = index[begin]
        cd = self.INFTY
        for i in range(begin, end):
            u = self.V[index[i]]
            if u.used and i + 1 < end:
                continue
            if u.angle - tmpAngle >= self.alpha or cnt >= self.treeSizes[curH] or i + 1 == end:
                r.cList.append(cv)
                self.build_tree(index, i - cnt, i + 1, self.V[cv], curH - 1)
                tmpAngle = u.angle
                cnt = 0
                cd = self.INFTY
            else:
                tmpD = self.get_dist(u.x, u.y, r.x, r.y)
                if tmpD < cd:
                    cd = tmpD
                    cv = index[i]
                cnt += 1


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
        print angle

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
    tree.build_tree(index, begin = 0, end = len(index), r = tree.V[0])
    tree.print_tree()
    tree.store_vertices('vertices')
    tree.store_edges('edges')

if __name__ == "__main__":
    main()