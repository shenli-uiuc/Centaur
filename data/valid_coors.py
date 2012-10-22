import math

f = open("coors", 'r')
fout = open("vcoors", "w")
for line in f:
    items = line.split(',')
    lat = float(items[0])
    lon = float(items[1])
    if math.fabs(lat) >= 90 or math.fabs(lon) > 180:
        continue
    fout.write("%f,%f\n"%(lat, lon))

f.close()
fout.close()
