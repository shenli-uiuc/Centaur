import time
try:
    import json
except ImportError,e:
    import simplejson as json

def main():
    f = open('/scratch/shenli3/data/sample', 'r')
    fout = open('/scratch/shenli3/data/extracted', 'w');
    
    isFirst = True
    baseT = 0
    for line in f:
        data = json.loads(line)
        if not 'text' in data.keys():
            continue
        x = time.strptime(data['created_at'],'%a %b %d %H:%M:%S +0000 %Y')
        t = time.mktime(x)
        if isFirst:
            isFirst = False
            baseT = t
        t -= baseT
        fout.write("%d, %d, %d, %d, %d, %d, %d\n"%(int(t), data['user']['id'], data['user']['followers_count'], data['user']['friends_count'], data['user']['statuses_count'], len(data['text']), len(line)))

    f.close()
    fout.close()

if __name__=='__main__':
    main()
