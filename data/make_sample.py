fin = open("vcoors", "r")
fout = open("small_coors", "w")

import random

sampleRate = 0.5
for line in fin:
    if random.random() > sampleRate:
        continue
    fout.write(line)
fin.close()
fout.close()
