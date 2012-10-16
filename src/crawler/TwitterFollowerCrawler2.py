try:
    import json
except ImportError,e:
    import simplejson as json

from MySQLDataStore import MySQLDataStore
from RateLimit import RateLimit
from TwitterUserCrawler import TwitterUserCrawler
import httplib

#crawls follower details: location, screen name, id
class TwitterFollowerCrawler:
    rateLimit = None
    mySQLDataStore = None
    userCrawler = None

    def __init__(self):
        self.rateLimit = RateLimit()
        self.mySQLDataStore = MySQLDataStore()
        self.userCrawler = TwitterUserCrawler()

    def remove_duplication(self, followerIDList):
        res = []
        for id in followerIDList:
            if not self.mySQLDataStore.check_user_by_id(id):
                res.append(id)
        print "*******************removed %d duplicate users"%(len(followerIDList) - len(res))
        return res

    def handle_one_followee(self, screenName):
        #get id from users table for the screenName
        id = self.mySQLDataStore.get_one_id(screenName)
        #get current offset in tmp_offset table
        curOffset = self.mySQLDataStore.select_cur_offset(id)
        #get max offset in follower_id table
        maxOffset = self.mySQLDataStore.select_max_offset(id)
        if maxOffset <= 0:
            print "User %s has not started yet!"%(screenName)
            return
        #if curOffset < maxOffset: pull data from curOffset
        print "before while"
        while curOffset < maxOffset:
            print "In while"
            curOffset += 1
            strFollowers = self.mySQLDataStore.select_follower_piece(id, curOffset) 
            if not strFollowers:
                print "Piece %d %d is missing!"%(id, curOffset)
                return
            listFollowers = json.loads(strFollowers)
#            listFollowers = self.remove_duplication(listFollowers)
            print ("++++++++++++++", screenName, curOffset, maxOffset, len(listFollowers))
            self.userCrawler.get_user_info(listFollowers, parameter = 'user_id')
            self.mySQLDataStore.update_cur_offset(id, curOffset) 

    def handle_all_followee(self, screenNameArr):
        for screenName in screenNameArr:
            self.handle_one_followee(screenName)

def main():
    f = open('sample.txt', 'r')
    names = []
    for line in f:
        names.append(line.split('\n')[0])
    names.reverse()
    names = ['rihanna', 'Cristiano']

    crawler = TwitterFollowerCrawler();
    crawler.handle_all_followee(names)

if __name__=='__main__':
    main()

