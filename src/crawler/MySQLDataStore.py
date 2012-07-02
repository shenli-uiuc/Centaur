from MySQLTwitterData import MySQLTwitterData
import json
import MySQLdb

import db_conf

class MySQLDataStore:

    badCharSet = ["'", '"']
    filename = None
    db = None

    strInsert2User = """INSERT INTO %s VALUES(%d, '%s', %d, '%s')"""
    strInsert2Follower = """INSERT INTO %s VALUES(%d, '%s', '%s', '%s')"""
    strInsert2Data = """INSERT INTO %s VALUES(%d, '%s', '%s', '%s')"""
    strSelectByID  = """SELECT * FROM %s WHERE id = %d"""
    strSelectAllID = """SELECT id FROM %s"""
    strSelectIDByName = """SELECT id FROM %s WHERE screen_name='%s'"""
    strSelectNCursor = """SELECT next_cursor from %s WHERE id = %d and previous_cursor = %s"""
    StrSelectMaxNCursor = """SELECT """

    def __init__(self):
        self.db = MySQLdb.connect(db_conf.host, db_conf.usr, db_conf.pwd, db_conf.dbName, charset='utf8')

    def store(self, userID, screenName, followerID, location):
        c = self.db.cursor()
        c.execute(self.strInsert2Data%(db_conf.dataTable, userID, screenName, json.dumps(followerID), location))

        # To improve efficiency, the commit function should be used in a batched way
        self.db.commit()
        c.close()

    def store_follower_piece(self, userID, pCursor, nCursor, followerID):
        c = self.db.cursor()
        c.execute(self.strInsert2Follower%(db_conf.followerTable, userID, pCursor, nCursor, json.dumps(followerID)))
        self.db.commit()
        c.close() 

    def check_follower_piece(self, userID, pCursor):
        c = self.db.cursor()
        cmd = self.strSelectNCursor%(db_conf.followerTable, userID, pCursor)
        c.execute(cmd)
        rows = c.fetchall()
        if len(rows):
            return int(rows[0][0])
        else:
            return None
        
    def _validate_str(self, rawStr):
        if not rawStr:
            return rawStr
        for c in self.badCharSet:
            rawStr = rawStr.replace(c, '_')
        return rawStr

    def store_user(self, userID, screenName, followerNum, location):
        c = self.db.cursor()
        cmd = self.strSelectByID%(db_conf.userTable, userID)
        c.execute(cmd)
        rows = c.fetchall()
        if len(rows):
            print "user %s already exist!"%(screenName)
            return
        print location
        location = self._validate_str(location)
        print location
        cmd = self.strInsert2User%(db_conf.userTable, userID, screenName, followerNum, location)
        print cmd
        c.execute(cmd)
        self.db.commit()
        c.close()

    def get_one_user(self, userID):
        c = self.db.cursor()
        c.execute(self.strSelectByID%(db_conf.dataTable, userID))
        rows = c.fetchall()
        res = []
        for row in rows:
            res.append((int(row[0]), row[1], row[2], row[3]))

        return res

    def get_all_id(self):
        c = self.db.cursor()
        c.execute(self.strSelectAllID%(db_conf.dataTable))
        rows = c.fetchall()

        res = []
        for row in rows:
        	res.append(int(row[0]))
        return res

    def get_one_id(self, screenName):
        c = self.db.cursor()
        c.execute(self.strSelectIDByName%(db_conf.userTable, screenName))
        rows = c.fetchall()
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
    simpleDataStore = MySQLDataStore()
    #two functions are now supported:
    #1. get_all_id: will return a list containing all user ids
    print simpleDataStore.get_all_id()

    #2. get_one_user: specify the user id, and will return the correponding data as a tuple. (see the print result)
    for userID in simpleDataStore.get_all_id():
        print simpleDataStore.get_one_user(userID)

    print simpleDataStore.check_follower_piece(100, 0)
    print simpleDataStore.check_follower_piece(100, 3)
    #print simpleDataStore.check_follower_piece(100, 7)
    print simpleDataStore.get_one_id('ladygaga')
    print simpleDataStore.get_one_id('justinbieber')
    print simpleDataStore.get_one_id('lianghai')
    simpleDataStore.close()

if __name__ == '__main__':
    main()










