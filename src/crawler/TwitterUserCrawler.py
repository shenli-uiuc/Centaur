try:
    import json
except ImportError,e:
    import simplejson as json

import urllib2
from MySQLDataStore import MySQLDataStore
from RateLimit import RateLimit
from URLHandler import URLHandler
import time

class TwitterUserCrawler:

    parameters = {'user_id':'user_id', 'screen_name':'screen_name'}
    urlUserLookup = "https://api.twitter.com/1/users/lookup.json?%s=%s"    
    dataStore = None
    rateLimit = None
    urlHandler = None

    def __init__(self):
        self.dataStore = MySQLDataStore()
        self.rateLimit = RateLimit()
        self.urlHandler = URLHandler()

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


    def dump_resp(self, url):
        retry = True
        while retry:
            try:
                retry = False
                rawData = self.urlHandler.open_url(url)
                if not rawData:
                    return
                data = json.loads(rawData.read())
                return data
            except ValueError, e:
                print ("ValueError: ",  e.message)
                retry = True


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
        data = self.dump_resp(url)
        if not data:
            return
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
        time.sleep(5)
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
