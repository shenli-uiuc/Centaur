import urllib2
import time
import os
import re
import sys
from MySQLTwitterData import MySQLTwitterData
from MySQLDataStore import MySQLDataStore
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

    def __init__(self, logName):
        self.logFile = open(logName,"w")
        self.db = MySQLDataStore()

    def open_url_followerID(self,url,screenName):
        count = 1
        while (count):
            if (count == 10):
                self.logFile.write("URL exceptions occur in %s: %s\n"%(screenName,url))
                return None                 
            try: 
                res = urllib2.urlopen(url)
                return res
            except urllib2.URLError, e:
                self.logFile.write(e.strerror)
                count = count + 1
                time.sleep(5)
                
    def open_url_limit(self,url):
        count = 1
        while (count):
            if (count == 10):
                self.logFile.write("Error in requesting: %s\n"%(url))
                self.clean_up()
                sys.exit()
            try:
                res = urllib2.urlopen(url)
                return res
            except urllib2.URLError,e:
                self.logFile.write(e.strerror)
                count = count + 1
            
 
    def check_limit(self):
        url = self.urlCheckLimit
        res = self.open_url_limit(url)
        data = json.loads(res.read())
        limit = data['remaining_hits']
        wakeup = data['reset_time_in_seconds']
        return (limit,wakeup)

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

    def get_follower_id(self, screenName, userID, cursor):	   
        screenName = screenName.split('\n')[0] #works for sample.txt
	 
        while cursor != 0: 
            (limit,wakeup) = self.check_limit()
            if (limit == 0):  
                interval = wakeup-time.time()
                time.sleep(interval)

            (pCursor,nCursor,ids) = self.get_one_page_id(screenName,cursor)
            print (screenName, userID, pCursor, nCursor)
		
            if ids == 0 and pCursor == 0 and nCursor == 0:
                return 
            self.db.store_follower_piece(userID,pCursor,nCursor,ids)
            cursor = nCursor


    def get_one_page_id(self, screenName, cursor):
        print ('0', screenName, cursor)
        url = self.urlGetFollowerID%(cursor, screenName)
        res = self.open_url_followerID(url,screenName) 
        if res == None:
            print "Fatal error: follower id page return None!!!"
            return (0, 0, 0)
        strData = res.read() 
        data = json.loads(strData)
        if 'errors' in data.keys():
            self.logFile.write("Errors in requesting %s: %s\n",(screenName, url))
            return (0,0,0)
        ids = data['ids']
        # the cursor is int64, I have used big int in the follower_id table -- Shen Li
        nCursor = data['next_cursor']
        pCursor = data['previous_cursor']
        print ('1', screenName, nCursor, len(ids))
        return (pCursor, nCursor,ids)        

    def get_all_follower_id(self,filename):
        inputFile = open(filename,"r")
        for line in inputFile:
            screenName = line.split('\n')[0]
            userID = self.db.get_one_id(screenName)
            cursor = self.db.get_next_cursor(userID)
            print ('2', screenName, cursor)
            self.get_follower_id(screenName,userID,cursor) 
        inputFile.close()
                    

    def clean_up(self):
        self.logFile.close()
        self.db.close()
    

def main():
    crawler = Crawler("log.txt")
    #ids = crawler.get_follower_id("lianghai")
    #crawler.get_screen_name('input.txt','screenName.txt')
    crawler.get_all_follower_id('sample.txt')
    crawler.clean_up()


if __name__=='__main__':
    main()
        
