from sets import Set

fin = open('gastweets-sources.txt', 'r')
fout = open('clean-source.txt', 'w')

ids = Set()

for line in fin:
    id = int(line)
    ids.add(id)

print len(ids)

for id in ids:
    fout.write('%d'%(id))

fin.close()
fout.close()
