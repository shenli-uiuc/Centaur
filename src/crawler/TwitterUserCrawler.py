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
        curList = []
        cnt = 0
        for name in screenNameArr:
            if 'user_id' == parameter and not self.dataStore.check_user_by_id(name):
                curList.append(name)
            else:
                cnt += 1
            if len(curList) >= 100:
                res = self.get_100_user_info(curList, parameter)
                if res:
                    self.store_users(res)
                else:
                    f = open("log/%f"%(time.time()), "w")
                    f.write(str(screenNameArr[cur:next]))
                    f.write("\n")
                    f.close()               
                curList = []            
        print ("removed", cnt, "users")    

        """
        while next < len(screenNameArr):
            res = self.get_100_user_info(screenNameArr[cur:next], parameter)
            if res:
                self.store_users(res)
            else:
                f = open("log/%f"%(time.time()), "w")
                f.write(str(screenNameArr[cur:next]))
                f.write("\n")
                f.close()
            cur = next
            next += 100

        if cur < len(screenNameArr):
            res = self.get_100_user_info(screenNameArr[cur:len(screenNameArr)], parameter)
            if res:
                self.store_users(res)
	    """
        

    def store_users(self, dictData):
        for screenName in dictData.keys():
            id = dictData[screenName]['id']
            loc = dictData[screenName]['location']
            followerNum = dictData[screenName]['followerNum']
            followeeNum = dictData[screenName]['followeeNum']
            statusNum = dictData[screenName]['statusNum']
            favorNum = dictData[screenName]['favorNum']
            createdAt = dictData[screenName]['createdAt']
            verified = dictData[screenName]['verified']
            #self.dataStore.store_user(id, screenName, folNum, loc)
            self.dataStore.store_user(id, screenName, followerNum, followeeNum, statusNum, favorNum, verified, createdAt, loc)

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
        #print ("after dumps:", strArr)
        strArr = strArr[1:len(strArr) - 1]
        strArr = ''.join(strArr.split())
        #print ("after join:", strArr)
        strArr = ''.join(strArr.split('"'))
        #print ("final:", strArr)
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
            res[screenName]['followeeNum'] = user['friends_count']
            res[screenName]['statusNum'] = user['statuses_count'] 
            res[screenName]['favorNum'] = user['favourites_count']
            res[screenName]['createdAt'] = user['favourites_count']
            if 'true' == user['verified']:
                res[screenName]['verified'] = True
            else:
                res[screenName]['verified'] = False
        time.sleep(5)
        return res
            
         
def main():
    f = open('sample_origin.txt', 'r')
    names = []
    for line in f:
        names.append(line.split('\n')[0])

    print names

    crawler = TwitterUserCrawler();
    crawler.get_user_info(names) 

if __name__=='__main__':
    main() 
