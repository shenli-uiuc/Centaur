#!/usr/bin/python
# -*- coding: utf-8 -*-


import MySQLdb

import apollo_conf
try:
    import json
except ImportError,e:
    import simplejson as json



class ApolloSQL:

    badCharSet = ["'", '"', '\\']
    filename = None
    db = None

    strInsert2Links = """INSERT IGNORE INTO internal_links VALUES(%s, %s)"""
    strUpdate2Cursor = """UPDATE internal_ncursor SET ncursor = %s WHERE followee_id = %s"""
    strSelectCursor = """SELECT ncursor FROM internal_ncursor WHERE followee_id = %s"""
    strInsert2Cursor = """INSERT INTO internal_ncursor VALUES(%s, %s)"""

    strInsert2User = """INSERT INTO users_complete VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)"""
    strInsert2Follower = """INSERT INTO follower_id VALUES(%s, %s, %s, %s, %s)"""
    strInsert2Data = """INSERT INTO twitter_data VALUES(%s, %s, %s, %s)"""
    strInsert2Tweet = """INSERT INTO tweet VALUES(%s, %s, %s, %s, %d, %d, %d)"""
    strInsert2Address = """INSERT IGNORE INTO address VALUE(%s, %s, %s, %s, %s)"""

    strSelectByID  = """SELECT * FROM %s WHERE id = %d"""
    strSelectAllID = """SELECT id FROM %s"""
    strSelectIDByName = """SELECT id FROM users_complete WHERE screen_name=%s"""
    strSelectNCursor = """SELECT next_cursor from %s WHERE id = %d and offset = %d"""
    strSelectMaxNCursor = """SELECT offset, next_cursor FROM %s WHERE id = %d AND offset = (SELECT MAX(offset) FROM follower_id WHERE id = %d)"""
    strSelectMaxOffset = """SELECT MAX(offset) FROM %s WHERE id = %d"""    
    strSelectMaxTweet = """SELECT MAX(tweet_id) from %s WHERE user_id = %d"""
    strSelectMinTweet = """SELECT MIN(tweet_id) from %s WHERE user_id = %d"""
    strSelectUserLoc = """SELECT location from users WHERE LENGTH(location) > 0 AND location != 'None' AND location > %s ORDER BY location LIMIT 1"""
    strSelectAddrLoc = """SELECT * from address WHERE location = %s"""
    strSelectUserCnt = """SELECT COUNT(*) from %s WHERE LENGTH(location) > 0 AND location != 'None'"""

    strSelectFollowerPiece = """SELECT follower_id FROM %s WHERE id = %d AND offset = %d"""

    strSelectLocation = """SELECT location, screen_name FROM %s WHERE id = %d"""

    strSelectCurOffset = """SELECT offset from %s WHERE id = %d"""
    strUpdateCurOffset = """UPDATE %s SET offset = %d WHERE id = %d"""
    strInsertCurOffset = """INSERT INTO %s VALUES(%d, %d)"""

    def __init__(self):
        self.db = MySQLdb.connect(apollo_conf.host, apollo_conf.usr, apollo_conf.pwd, apollo_conf.dbName, charset='utf8')

    def store_page_link(self, followee_id, ids, nCursor):
        c = self.db.cursor()
        for id in ids:
            c.execute(self.strInsert2Links, (followee_id, id))

        self.db.commit()
        c.close()

        self.update_ncursor(followee_id, nCursor)

    def new_ncursor(self, followee_id):
        c = self.db.cursor()
        c.execute(self.strInsert2Cursor, (followee_id, -1))

        self.db.commit()
        c.close()

    def update_ncursor(self, followee_id, nCursor):        

        c = self.db.cursor()
        c.execute(self.strUpdate2Cursor, (nCursor, followee_id))

        self.db.commit()
        c.close()

    #deprecated
    def store(self, userID, screenName, followerID, location):
        c = self.db.cursor()
        c.execute(self.strInsert2Data, (userID, screenName, json.dumps(followerID), location))

        # To improve efficiency, the commit function should be used in a batched way
        self.db.commit()
        c.close()

    def store_follower_piece(self, userID, offset, pCursor, nCursor, followerID):
        c = self.db.cursor()
        c.execute(self.strInsert2Follower, (userID, offset, pCursor, nCursor, json.dumps(followerID)))
        self.db.commit()
        c.close() 

    def select_follower_piece(self, userID, offset):
        c = self.db.cursor()
        c.execute(self.strSelectFollowerPiece%(db_conf.followerTable, userID, offset))
        rows = c.fetchall()
        c.close()
        if len(rows):
            return rows[0][0]
        else:
            return None

    #select on non-empty location
    def select_user_location_offset(self, prev_loc):
        c = self.db.cursor()
        c.execute(self.strSelectUserLoc, (prev_loc))
        rows = c.fetchall()
        c.close()
        if len(rows[0][0]):
            return rows[0][0]
        else:
            return None

    def select_ncursor(self, followee_id):
        c = self.db.cursor()
        c.execute(self.strSelectCursor, (followee_id))
        rows = c.fetchall()
        c.close()
        if len(rows):
            return int(rows[0][0])
        else:
            self.new_ncursor(followee_id)
            return -1

    #get the number of users in users table
    def select_user_count(self):
        c = self.db.cursor()
        c.execute(self.strSelectUserCnt%(db_conf.userTable))
        rows = c.fetchall()
        c.close()
        return int(rows[0][0])

    #select location from address table
    def select_addr_location(self, location):
        location = unicode(location, 'latin-1')
        c = self.db.cursor()
        c.execute(self.strSelectAddrLoc, (location))
        rows = c.fetchall()
        c.close()
        if len(rows):
            return rows[0]
        else:
            return None



    #insert one address
    def insert_address(self, location, latitude, longitude, formatted, types):
        location = unicode(location, 'latin-1')
        if formatted:
            for c in self.badCharSet:
                formatted = formatted.replace(c, '_')

        c = self.db.cursor()
        c.execute(self.strInsert2Address, (location, latitude, longitude, formatted, types))
        c.close()
        self.db.commit()



    #get the max tweet id of one specific user in database
    def select_max_tweet(self, userID):
        c = self.db.cursor()
        c.execute(self.strSelectMaxTweet%(db_conf.tweetTable, userID))
        rows = c.fetchall()
        c.close()
        if rows[0][0]:
            return int(rows[0][0])
        else:
            return 0

    def select_min_tweet(self, userID):
        c = self.db.cursor()
        c.execute(self.strSelectMinTweet%(db_conf.tweetTable, userID))
        rows = c.fetchall()
        c.close()
        if rows[0][0]:
            return int(rows[0][0])
        else:
            return (2 ** 63) - 1


    #insert one tweet into database
    def insert_tweet(self, tweetID, userID, createdAt, text, retweetCount, retweeted, pullAt):
        for c in self.badCharSet:
            text = text.replace(c, '_')
        c = self.db.cursor()
        c.execute(self.strInsert2Tweet, (userID, createdAt, text, retweetCount, retweeted, pullAt))
        c.close()
        self.db.commit()

    #get the location from users table with the given user id
    def select_user_location(self, userID):
        c = self.db.cursor()
        c.execute(self.strSelectLocation%(db_conf.userTable, userID))
        rows = c.fetchall()
        c.close()
        if len(rows):
            if rows[0][0] and len(rows[0][0]) > 0:
                return rows[0][0]
            else:
                return 'No Location'
        else:
            return None




    #get next_cursor to pull the follower id list from follower_id table
    def get_next_cursor(self, userID):
        c = self.db.cursor()
        c.execute(self.strSelectMaxNCursor%(db_conf.followerTable, userID, userID))
        rows = c.fetchall()
        c.close()
        if len(rows):
            return (int(rows[0][0]), int(rows[0][1])) 
        else:
            return (0, -1)

    #get max offset of a given user
    def select_max_offset(self, userID):
        c = self.db.cursor()
        c.execute(self.strSelectMaxOffset%(db_conf.followerTable, userID))
        rows = c.fetchall()
        c.close()
        if len(rows):
            return int(rows[0][0])
        else:
            return -1

    #check current offset from tmp_offset table to see which piece of followers' locations should we pull
    def select_cur_offset(self, userID):
        c = self.db.cursor()
        c.execute(self.strSelectCurOffset%(db_conf.tmpOffsetTable, userID))
        rows = c.fetchall()
        c.close()
        if len(rows):
            return int(rows[0][0])
        else:
            self.insert_cur_offset(userID, 0)
            return 0

    def update_cur_offset(self, userID, curOffset):
        c = self.db.cursor()
        c.execute(self.strUpdateCurOffset%(db_conf.tmpOffsetTable, curOffset, userID))
        c.close()
        self.db.commit()

    def insert_cur_offset(self, userID, curOffset):
        c = self.db.cursor()
        c.execute(self.strInsertCurOffset%(db_conf.tmpOffsetTable, userID, curOffset))
        c.close()
        self.db.commit()

    def check_follower_piece(self, userID, offset):
        pCursor = int(pCursor)
        c = self.db.cursor()
        cmd = self.strSelectNCursor%(db_conf.followerTable, userID, offset)
        c.execute(cmd)
        rows = c.fetchall()
        c.close()
        if len(rows):
            return rows[0][0]
        else:
            return None
        
    def _validate_str(self, rawStr):
        if not rawStr:
            return rawStr
        for c in self.badCharSet:
            rawStr = rawStr.replace(c, '_')
        return rawStr

    def check_user_by_id(self, userID):
        c = self.db.cursor()
        cmd = self.strSelectByID%(db_conf.userTableComplete, userID)
        c.execute(cmd)
        rows = c.fetchall()
        c.close()
        if len(rows):
            return True
        else:
            return False


    def store_user(self, userID, screenName, followerNum, followeeNum, statusNum, favorNum, verified, createdAt, location):
    #def store_user(self, userID, screenName, followerNum, location):
        c = self.db.cursor()
        cmd = self.strSelectByID%(db_conf.userTableComplete, userID)
        c.execute(cmd)
        rows = c.fetchall()
        if len(rows):
            print "user %s already exist!"%(screenName)
            c.close()
            return
        #print location
        location = self._validate_str(location)
        #print location
        #cmd = self.strInsert2User%(db_conf.userTable, userID, screenName, followerNum, location)
        #print cmd
        c.execute(self.strInsert2User, (userID, screenName, followerNum, followeeNum, statusNum, favorNum, verified, createdAt, location))
        self.db.commit()
        c.close()

    def get_one_user(self, userID):
        c = self.db.cursor()
        c.execute(self.strSelectByID%(db_conf.dataTable, userID))
        rows = c.fetchall()
        c.close()
        res = []
        for row in rows:
            res.append((int(row[0]), row[1], row[2], row[3]))

        return res

    def get_all_id(self):
        c = self.db.cursor()
        c.execute(self.strSelectAllID%(db_conf.dataTable))
        rows = c.fetchall()
        c.close()

        res = []
        for row in rows:
        	res.append(int(row[0]))
        return res

    def get_one_id(self, screenName):
        c = self.db.cursor()
        c.execute(self.strSelectIDByName, (screenName))
        rows = c.fetchall()
        c.close()
        if len(rows):
            return int(rows[0][0])
        else:
            return None    
      

    def close(self):
        if self.db:
            self.db.close()
        
        
def main():
    """
    #Test Write

    #Specify a file path to store the database data
    dbName = 'test.db'
    #Create a MySQLDataStore object. True means this call will create a new database, one error will raise if the database already exists.
    simpleDataStore = MySQLDataStore()
    #tmpData = MySQLTwitterData(1826, 'uiuc',  [19, 23, 25, 668], 'Champaign');
    #Store the data of one user. The parameters are (userName(string), userID(int), followerID(int list), followerPos(int list, each element is a list with two elements, namely x, and y coordination))
    #simpleDataStore.store(tmpData.userID, tmpData.screenName, tmpData.followerID, tmpData.location)
    #tmpData = MySQLTwitterData(1829, 'umich', [19, 23, 25, 668, 890], 'Michigan') 
    #simpleDataStore.store(tmpData.userID, tmpData.screenName, tmpData.followerID, tmpData.location)
    #Close the db connection when you do not need it any more

    simpleDataStore.store_follower_piece(100, 0, 3, [0, 1, 2])
    simpleDataStore.store_follower_piece(100, 3, 7, [3, 4, 5, 6])

    simpleDataStore.store_user(0, 'test1', 10, 'Beijing, China')
    simpleDataStore.store_user(1, 'test2', 15, 'Shanghai, China')

    simpleDataStore.close()
    """
    #test read
    #False means this call will not create a new db
    apolloSQL = ApolloSQL()

    #apolloSQL.store_page_link(1000, 1001)
    print apolloSQL.select_ncursor(1000)
    print apolloSQL.select_ncursor(1000)
    apolloSQL.update_ncursor(1000, 500)
    print apolloSQL.select_ncursor(1000)

    apolloSQL.store_page_link(1000, [1, 2], 900)
    print apolloSQL.select_ncursor(1000)    

    #two functions are now supported:
    #1. get_all_id: will return a list containing all user ids
    apolloSQL.close()

if __name__ == '__main__':
    main()










