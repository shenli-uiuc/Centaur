from MySQLTwitterData import MySQLTwitterData
import json
import MySQLdb

import db_conf

class MySQLDataStore:

    _dbName = 'twitter_data'

    filename = None
    db = None

    strInsertValue = """INSERT INTO %s VALUES(%d, '%s', '%s', '%s')"""
    strSelectByID  = """SELECT * From %s WHERE id = %d"""
    strSelectAllID = """SELECT id FROM %s"""

    def __init__(self, filename, create = False):
        self.filename = filename
        self.db = MySQLdb.connect(db_conf.host, db_conf.usr, db_conf.pwd, db_conf.dbName)

    def store(self, userID, screenName, followerID, location):
        followerNum = len(followerID)
        c = self.db.cursor()
        c.execute(self.strInsertValue%(db_conf.tableName, userID, screenName, json.dumps(followerID), location))

        # To improve efficiency, the commit function should be used in a batched way
        self.db.commit()
        c.close()

    def get_one_user(self, userID):
        c = self.db.cursor()
        c.execute(self.strSelectByID%(db_conf.tableName, userID))
        rows = c.fetchall()
        res = []
        for row in rows:
            res.append((int(row[0]), row[1], row[2], row[3]))

        return res

    def get_all_id(self):
        c = self.db.cursor()
        c.execute(self.strSelectAllID%(db_conf.tableName))
        rows = c.fetchall()

        res = []
        for row in rows:
            res.append(int(row[0]))

        return res

    def close(self):
        if self.db:
            self.db.close()
        
        
def main():

    #Test Write

    #Specify a file path to store the database data
    dbName = 'test.db'
    #Create a MySQLDataStore object. True means this call will create a new database, one error will raise if the database already exists.
    simpleDataStore = MySQLDataStore(dbName, True)
    tmpData = MySQLTwitterData(1826, 'uiuc',  [19, 23, 25, 668], 'Champaign');
    #Store the data of one user. The parameters are (userName(string), userID(int), followerID(int list), followerPos(int list, each element is a list with two elements, namely x, and y coordination))
    simpleDataStore.store(tmpData.userID, tmpData.screenName, json.dumps(tmpData.followerID), tmpData.location)
    tmpData = MySQLTwitterData(1829, 'umich', [19, 23, 25, 668, 890], 'Michigan') 
    simpleDataStore.store(tmpData.userID, tmpData.screenName, json.dumps(tmpData.followerID), tmpData.location)
    #Close the db connection when you do not need it any more
    simpleDataStore.close()

    #test read
    #False means this call will not create a new db
    simpleDataStore = MySQLDataStore(dbName, False)
    #two functions are now supported:
    #1. get_all_id: will return a list containing all user ids
    print simpleDataStore.get_all_id()

    #2. get_one_user: specify the user id, and will return the correponding data as a tuple. (see the print result)
    for userID in simpleDataStore.get_all_id():
        print simpleDataStore.get_one_user(userID)

    simpleDataStore.close()

if __name__ == '__main__':
    main()










