f = open("extracted", "r");
fout = open("shrinked", "w")

for line in f:
    items = line.split(", ")
    timestamp = int(items[0])
    folNum = int(items[2])
    msgLen = int(items[6])
    fout.write("%d,%d,%d\n"%(timestamp, folNum, msgLen));

f.close()
fout.close()
