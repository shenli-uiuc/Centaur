try:
    import json
except ImportError,e:
    import simplejson as json

import urllib2
from MySQLDataStore import MySQLDataStore

class TwitterUserCrawler:

    urlUserLookup = "https://api.twitter.com/1/users/lookup.json?screen_name=%s"    
    dataStore = None

    def __init__(self):
        self.dataStore = MySQLDataStore()

    def get_user_info(self, screenNameArr):
        cur = 0
        next = 100

        while next < len(screenNameArr):
            res = self.get_100_user_info(screenNameArr[cur:next])
            self.store_users(res)
            cur = next
            next += 100

    def store_users(self, dictData):
        for screenName in dictData.keys():
            id = dictData[screenName]['id']
            loc = dictData[screenName]['location']
            folNum = dictData[screenName]['followerNum']
            self.dataStore.store_user(id, screenName, folNum, loc)


    def get_100_user_info(self, screenNameArr):
        if len(screenNameArr) > 100:
            print "TwitterUserCrawler:get_100_user_info accepts at most 100 screen names"
            exit(0)
        strArr = json.dumps(screenNameArr)
        strArr = strArr[1:len(strArr) - 1]
        strArr = ''.join(strArr.split())
        strArr = ''.join(strArr.split('"'))
        url = self.urlUserLookup%(strArr)
        print url
        rawData = urllib2.urlopen(url)
        data = json.loads(rawData.read())
        res = {}
        for user in data:
            if 'errors' in user.keys():
                print "one error occur"
                continue
            screenName = user['screen_name']
            res[screenName] = {}
            res[screenName]['id'] = user['id']
            res[screenName]['location'] = user['location']
            res[screenName]['followerNum'] = user['followers_count']

        return res
            
         
def main():
    f = open('screenName.txt', 'r')
    names = []
    for line in f:
        names.append(line.split('\n')[0])

    print names

    crawler = TwitterUserCrawler();
    crawler.get_user_info(names) 


if __name__=='__main__':
    main() 
