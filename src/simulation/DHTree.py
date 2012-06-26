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
        for coor in coors:
            curV = Vertex(coor[0], coor[1])
            self.V.append(curV)

    def _init_tree_sizes(self):
        for i in range(self.h + 1):
            self.treeSizes.append((self.d ** i - 1) / (self.d - 1))

    def build_tree(self, index, begin, end, r, curH):
        if curH <= 2:
            for i in range(begin, end):
                if self.V[index[i]] == r:
                    continue
                r.cList.append(index[i])
            return

        for i in range(begin, end):
            u = self.V[index[i]]
            u.angle = self.get_angle(u.x, u.y, r.x, r.y)

        index[begin:end] = sorted(index[begin:end], key = _comp)

        tmpAngle = 0
        cnt = 0
        cv = index[begin]
        cd = self.INFTY
        for i in range(begin, end):
            u = self.V[index[i]]
            if u == r:
                continue
            if u.angle - tmpAngle >= self.alpha or cnt >= self.treeSizes[curH]:
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


    def _comp(self, a, b):
        return V[a].angle < V[b].angle


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

        return angle

class Vertex:
    x = 0
    y = 0
    angle = 0
    cList = []

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.cList = []

    def __str__(self):
        return json.dumps((x, y, angle, cList))    

def main():
    nodeGenerator = NodeGenerator()
    coors = nodeGenerator.gen(10, 100) 
    tree = DHTree(2, 7, math.pi * 2, coors)
    print tree.V

if __name__ == "__main__":
    main()
