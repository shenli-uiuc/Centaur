import urllib2
import time
import os
import re
import sys
from MySQLDataStore import MySQLDataStore
from URLHandler import URLHandler
try:
    import json
except ImportError,e:
    import simplejson as json


class Crawler:
    
    logFile = None 
    db = None

    urlGetFollowerID = "https://api.twitter.com/1/followers/ids.json?cursor=%d&screen_name=%s"  
    urlCheckLimit = "https://api.twitter.com/1/account/rate_limit_status.json"
    # for 1 user: id, screen name, name 
    urlSingleUserInfo = "https://api.twitter.com/1/users/show.json?screen_name=%s&include_entities=true" 
    # up to 100 users: returns a list, data[0]['name'] include_entities = true?
    urlUserInfo = "https://api.twitter.com/1/users/lookup.json?include_entities=true&screen_name=%s"

    urlHandler = None

    def __init__(self, logName):
        self.logFile = open(logName,"w")
        self.db = MySQLDataStore()
        self.urlHandler = URLHandler()
    
    """
    def open_url_followerID(self,url,screenName):
        count = 1
        while (count):
            if (count == 10):
                self.logFile.write("URL exceptions occur in %s: %s\n"%(screenName,url))
                return None                 
            try: 
                res = urllib2.urlopen(url)
                return res
            except urllib2.HTTPError, e:
                self.logFile.write(str(e.strerror, e.message))
                count = count + 1
                time.sleep(5)
            except urllib2.URLError, e:
                self.logFile.write(e.reason)
                #self.logFile.write(e.strerror)
                count = count + 1
                time.sleep(5)
    """        
 
    def check_limit(self):
        url = self.urlCheckLimit
        res = self.urlHandler.open_url(url)
        data = json.loads(res.read())
        limit = data['remaining_hits']
        wakeup = data['reset_time_in_seconds']
        return (limit,wakeup)

    """
    def get_user_info(self,follower_sname_list):
        #construct sname-list seperated by ,
        url = self.urlUserInfo
        #check rate limit
        res = self.open_url(url)
        return json.loads(res.read())

    
    def get_follower_location(self,follower_sname_list):
        locations = []
        data = self.get_user_info(follower_sname_list)
        for i in range(len(follower_sname_list)):
            locations.append(data[i]['location'])
        return locations         
    """

    def create_file(self,screenName,i):
        if not os.path.isdir("./"+screenName+"/"):
            os.mkdir("./"+screenName+"/")
        outputFile = open("./%s/followerID%d.txt"%(screenName,i),"w")
        return outputFile

    def get_screen_name(self,in_filename,out_filename):
        inputFile = open(in_filename,"r")
        outputFile = open(out_filename,"w")
        for line in inputFile:
            name = re.split(r'[()]',line)
            outputFile.write(name[1]+'\n')

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
            self.logFile.write("Fatal Errors in requesting %s: %s\n",(screenName, url))
            return (0, 0, 0)
        strData = res.read() 
        data = json.loads(strData)
        if 'errors' in data.keys():
            print "Fatal Errors: follower id page return None!!!"
            self.logFile.write("Fatal Errors in requesting %s: %s\n",(screenName, url))
            return (0,0,0)
        ids = data['ids']
        # the cursor is int64, I have used big int in the follower_id table -- Shen Li
        nCursor = data['next_cursor']
        pCursor = data['previous_cursor']
        return (pCursor, nCursor,ids)        

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
    crawler.get_all_follower_id('sample3.txt')
    crawler.clean_up()


if __name__=='__main__':
    main()
        
