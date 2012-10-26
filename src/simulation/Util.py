import math

width = 40076.0
height = 40009.0
maxDist = 43000.0

maxNet = 10 * 1024
minNet = 128

#input: coordination, output: distance on earth surface
def distance(origin, destination):
    lat1, lon1 = origin
    lat2, lon2 = destination
    radius = 6371 # km

    dlat = math.radians(lat2-lat1)
    dlon = math.radians(lon2-lon1)
    a = math.sin(dlat/2) * math.sin(dlat/2) + math.cos(math.radians(lat1)) \
        * math.cos(math.radians(lat2)) * math.sin(dlon/2) * math.sin(dlon/2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    d = radius * c

    return d

#from the sigcomm paper, rought
def delay(x1, y1, x2, y2):
    dist = math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)
    return (1.5 * dist) / (50.0 * 1000.0)

def net(x1, y1, x2, y2):
    dist = math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)
    if dist > maxDist:
        return minNet
    return maxNet - maxNet * math.sqrt(dist/maxDist)


#translate latitude and longitude to 2D coordinations
def loc2coor(latitude, longitude):
    x = (((longitude + 180) * width)/360) % width
    y = height / 2 - math.log( math.tan((latitude+90) * math.pi /360) )*width/(2* math.pi)
    return (x, y)
