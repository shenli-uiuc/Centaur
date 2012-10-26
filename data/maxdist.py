import math

width = 40076.0
height = 40009.0


def loc2coor(latitude, longitude):
    x = (((longitude + 180) * width)/360) % width
    y = height / 2 - math.log( math.tan((latitude+90) * math.pi /360) )*width/(2* math.pi)
    return (x, y)


f = open("vcoors", "r")
xys = []

cnt = 0
for line in f:
    cnt += 1
    if cnt >= 10000:
        break
    items = line.split(",")
    x = float(items[0])
    y = float(items[1])
    x, y = loc2coor(x, y)
    xys.append([x,y])

maxDist = 0
minDist = 99999999
for u in xys:
    for v in xys:
        dist = (u[0] - v[0]) ** 2 + (u[1] - v[1]) ** 2
        if maxDist < dist:
            maxDist = dist
        if minDist > dist:
            minDist = dist

print math.sqrt(maxDist), math.sqrt(minDist)
