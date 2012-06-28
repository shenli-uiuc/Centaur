import urllib2
import simplejson as json
import time
import os
import re

class Crawler:

    urlGetFollowerID = "https://api.twitter.com/1/followers/ids.json?cursor=%d&screen_name=%s"  
    urlCheckLimit = "https://api.twitter.com/1/account/rate_limit_status.json"
    # for 1 user: id, screen name, name 
    urlSingleUserInfo = "https://api.twitter.com/1/users/show.json?screen_name=%s&include_entities=true" 
    # up to 100 users: returns a list, data[0]['name'] include_entities = true?
    urlUserInfo = "https://api.twitter.com/1/users/lookup.json?include_entities=true&screen_name=%s"
 
    def check_limit(self):
        url = self.urlCheckLimit
        res = urllib2.urlopen(url)
        data = json.loads(res.read())
        limit = data['remaining_hits']
        return limit

    def get_user_info(self,follower_sname_list):
        #construct sname-list seperated by ,
        url = self.urlUserInfo
        #check rate limit
        res = urllib2.urlopen(url)
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

    def get_follower_id(self, screenName):
        cursor = -1
        id_list = []
        i = 0
        outputFile = self.create_file(screenName,i)
        while (cursor):
            limit = self.check_limit()
            if (limit == 0):
                outputFile.close()
                i = i+1
                outputFile = self.create_file(screenName,i)
                time.sleep(3600)

            (ids,nextCursor) = self.get_one_page_id(screenName,cursor)
            id_list.extend(ids)
            for follower_id in ids:
                outputFile.write("%d\n"%(follower_id))
            cursor = nextCursor

        # cursor = 0, we are at the last page
        (ids,nextCursor) = self.get_one_page_id(screenName,cursor)
        id_list.extend(ids)
        for follower_id in ids:
            outputFile.write("%d\n"%(follower_id))
        outputFile.close()
        return id_list


    def get_one_page_id(self, screenName, cursor):
        url = self.urlGetFollowerID%(cursor, screenName)
        res = urllib2.urlopen(url) 
        strData = res.read() 
        data = json.loads(strData)
        ids = data['ids']
        nextCursor = data['next_cursor']
        return (ids, nextCursor)        

    def get_all_follower_id(self,filename):
       inputFile = open(filename,"r")
       for line in inputFile:
           self.get_follower_id(line)


def main():
    crawler = Crawler()
    #crawler.get_follower_id("lianghai")
    crawler.get_screen_name('input.txt','screenName.txt')
    crawler.get_all_follower_id('screenName.txt')

if __name__=='__main__':
    main()
        
