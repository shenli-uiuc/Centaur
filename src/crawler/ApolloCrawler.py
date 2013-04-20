import urllib2
import time
import os
import re
import sys
from sets import Set
from ApolloSQL import ApolloSQL
from URLHandler import URLHandler
try:
    import json
except ImportError,e:
    import simplejson as json


class Crawler:

    idFile = "/home/tarek/shenli3/project/Centaur/src/crawler/gastweets-sources.txt"    
    idSet = Set()
    logFile = None 
    db = None

    urlGetFollowerID = "https://api.twitter.com/1/followers/ids.json?cursor=%d&id=%s"  
    urlCheckLimit = "https://api.twitter.com/1/account/rate_limit_status.json"
    # for 1 user: id, screen name, name 
    urlSingleUserInfo = "https://api.twitter.com/1/users/show.json?screen_name=%s&include_entities=true" 
    # up to 100 users: returns a list, data[0]['name'] include_entities = true?
    urlUserInfo = "https://api.twitter.com/1/users/lookup.json?include_entities=true&screen_name=%s"

    urlHandler = None

    def __init__(self, logName):
        fin = open(self.idFile, "r")
        for line in fin:
            self.idSet.add(int(line))
        fin.close()

        self.logFile = open(logName,"w")
        self.db = ApolloSQL()
        self.urlHandler = URLHandler()
    
 
    def check_limit(self):
        url = self.urlCheckLimit
        res = self.urlHandler.open_url(url)
        data = json.loads(res.read())
        limit = data['remaining_hits']
        wakeup = data['reset_time_in_seconds']
        return (limit,wakeup)

    def create_file(self,screenName,i):
        if not os.path.isdir("./"+screenName+"/"):
            os.mkdir("./"+screenName+"/")
        outputFile = open("./%s/followerID%d.txt"%(screenName,i),"w")
        return outputFile

    def get_link(self, followee_id):
        followee_id = int(followee_id)

        cursor = self.db.select_ncursor(followee_id)   
 
        while cursor != 0:
            (limit, wakeup) = self.check_limit()
            while limit == 0:
                interval = wakeup - time.time()
                time.sleep(interval)
                time.sleep(30)
                (limit, wakeup) = self.check_limit()

            (pCursor, nCursor, ids) = self.get_one_page_id(followee_id, cursor)
            print(followee_id, pCursor, nCursor)

            if ids == 0 and pCursor == 0 and nCursor == 0:
                self.db.store_page_link(followee_id, [], 0)
                return
            newIds = []
            for id in ids:
                if id in self.idSet:
                    newIds.append(id)

            self.db.store_page_link(followee_id, newIds, nCursor)
            cursor = nCursor

    def get_follower_id(self, screenName, userID, offset, cursor):	   
        screenName = screenName.split('\n')[0] #works for sample.txt
	 
        while cursor != 0: 
            offset += 1
            (limit,wakeup) = self.check_limit()
            while (limit == 0):  
                interval = wakeup-time.time()
                time.sleep(interval)
                time.sleep(30)
                (limit,wakeup) = self.check_limit()

            (pCursor,nCursor,ids) = self.get_one_page_id(screenName,cursor)
            print (screenName, userID, offset, pCursor, nCursor)
		
            if ids == 0 and pCursor == 0 and nCursor == 0:
                return 
            self.db.store_follower_piece(userID, offset, pCursor, nCursor, ids)
            cursor = nCursor


    def get_one_page_id(self, screenName, cursor):
        print ("Screen Name", screenName, "cursor", cursor)
        url = self.urlGetFollowerID%(cursor, screenName)
        print url
        res = self.urlHandler.open_url(url)
        if res == None:
            print "Fatal Errors: follower id page return None!!!"
            self.logFile.write("Fatal Errors in requesting %s: %s\n"%(screenName, url))
            return (0, 0, 0)
        strData = res.read() 
        data = json.loads(strData)
        if 'errors' in data.keys():
            print "Fatal Errors: follower id page return None!!!"
            self.logFile.write("Fatal Errors in requesting %s: %s\n"%(screenName, url))
            return (0,0,0)
        ids = data['ids']
        # the cursor is int64, I have used big int in the follower_id table -- Shen Li
        nCursor = data['next_cursor']
        pCursor = data['previous_cursor']
        return (pCursor, nCursor,ids)        

    def get_all_links(self, filename):
        fin = open(filename, 'r')
        for line in fin:
            followee_id = line.split('\n')[0]
            self.get_link(followee_id)

    def get_all_follower_id(self,filename):
        inputFile = open(filename,"r")
        for line in inputFile:
            screenName = line.split('\n')[0]
            userID = self.db.get_one_id(screenName)
            if not userID:
                continue
            (offset, cursor) = self.db.get_next_cursor(userID)
            self.get_follower_id(screenName, userID, offset, cursor) 
        inputFile.close()
                    

    def clean_up(self):
        self.logFile.close()
        self.db.close()
    

def main():
    crawler = Crawler("log.txt")
    #ids = crawler.get_follower_id("lianghai")
    #crawler.get_screen_name('input.txt','screenName.txt')
    crawler.get_all_links(sys.argv[1])
    crawler.clean_up()


if __name__=='__main__':
    main()
        
