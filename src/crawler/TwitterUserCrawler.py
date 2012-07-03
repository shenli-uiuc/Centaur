try:
    import json
except ImportError,e:
    import simplejson as json

import urllib2
from MySQLDataStore import MySQLDataStore
from RateLimit import RateLimit

class TwitterUserCrawler:

    parameters = {'user_id':'user_id', 'screen_name':'screen_name'}
    urlUserLookup = "https://api.twitter.com/1/users/lookup.json?%s=%s"    
    dataStore = None
    rateLimit = None


    def __init__(self):
        self.dataStore = MySQLDataStore()
        self.rateLimit = RateLimit()

    def get_user_info(self, screenNameArr, parameter = 'screen_name'):
        cur = 0
        next = 100
        print ("get_user_info: ", parameter)
        while next < len(screenNameArr):
            res = self.get_100_user_info(screenNameArr[cur:next], parameter)
            self.store_users(res)
            cur = next
            next += 100

        if cur < len(screenNameArr):
            res = self.get_100_user_info(screenNameArr[cur:len(screenNameArr)], parameter)
            self.store_users(res)
	    

    def store_users(self, dictData):
        for screenName in dictData.keys():
            id = dictData[screenName]['id']
            loc = dictData[screenName]['location']
            folNum = dictData[screenName]['followerNum']
            self.dataStore.store_user(id, screenName, folNum, loc)


    def get_100_user_info(self, screenNameArr, parameter):
        if len(screenNameArr) > 100:
            print "TwitterUserCrawler:get_100_user_info accepts at most 100 screen names"
            exit(0)
        print ("get_user_info: ", parameter, self.parameters[parameter])
        print "Crawling %d users"%(len(screenNameArr))
        strArr = json.dumps(screenNameArr)
        strArr = strArr[1:len(strArr) - 1]
        strArr = ''.join(strArr.split())
        strArr = ''.join(strArr.split('"'))
        url = self.urlUserLookup%(self.parameters[parameter], strArr)
        print url
        self.rateLimit.check()
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
    f = open('sample.txt', 'r')
    names = []
    for line in f:
        names.append(line.split('\n')[0])

    print names

    crawler = TwitterUserCrawler();
    crawler.get_user_info(names) 

if __name__=='__main__':
    main() 
