fin = open('shrinked', 'r')

sum = 0
for line in fin:
    items = line.split(',')
    sum += int(items[1])

print (sum, sum * 3 / 20000) 
