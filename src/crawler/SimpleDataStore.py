from TwitterData import TwitterData
import sqlite3
import simplejson as json

class SimpleDataStore:

    _dbName = 'twitter_data'

    filename = None
    db = None

    strCreateTable = """CREATE TABLE %s(user_id integer, screen_name text, user_name text, follower_num integer, 
                                        follower_id text, follower_pos text, 
                                        UNIQUE(user_id))"""
    strInsertValue = """INSERT INTO %s VALUES(?, ?, ?, ?, ?, ?)"""
    strSelectByID  = """SELECT * From %s WHERE user_id = %d"""
    strSelectAllID = """SELECT user_id FROM %s"""

    def __init__(self, filename, create = False):
        self.filename = filename
        self.db = sqlite3.connect(filename)
        if create:
            c = self.db.cursor()
            c.execute(self.strCreateTable%(self._dbName))
            self.db.commit()
            c.close()


    def store(self, userID, screenName, userName, followerID, followerPos):
        followerNum = len(followerID)
        c = self.db.cursor()
        c.execute(self.strInsertValue%(self._dbName), (userID, screenName, userName, followerNum, json.dumps(followerID), json.dumps(followerPos)))

        # To improve efficiency, the commit function should be used in a batched way
        self.db.commit()
        c.close()

    def get_one_user(self, userID):
        c = self.db.cursor()
        c.execute(self.strSelectByID%(self._dbName, userID))
        rows = c.fetchall()
        res = []
        for row in rows:
            res.append((int(row[0]), row[1], row[2], int(row[3]), json.loads(row[4]), json.loads(row[5])))

        return res

    def get_all_id(self):
        c = self.db.cursor()
        c.execute(self.strSelectAllID%(self._dbName))
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
    #Create a SimpleDataStore object. True means this call will create a new database, one error will raise if the database already exists.
    simpleDataStore = SimpleDataStore(dbName, True)
    tmpData = TwitterData(1826, 'screenuiuc', 'uiuc',  [19, 23, 25, 668], [[0, 0], [90, 48], [100, 150], [30, 15]]);
    #Store the data of one user. The parameters are (userName(string), userID(int), followerID(int list), followerPos(int list, each element is a list with two elements, namely x, and y coordination))
    simpleDataStore.store(tmpData.userID, tmpData.screenName, tmpData.userName, json.dumps(tmpData.followerID), json.dumps(tmpData.followerPos))
    tmpData = TwitterData(1829, 'screenumich', 'umich', [19, 23, 25, 668, 890], [[5, 5], [90, 48], [100, 150], [30, 15]]) 
    simpleDataStore.store(tmpData.userID, tmpData.screenName, tmpData.userName, json.dumps(tmpData.followerID), json.dumps(tmpData.followerPos))
    #Close the db connection when you do not need it any more
    simpleDataStore.close()

    #test read
    #False means this call will not create a new db
    simpleDataStore = SimpleDataStore(dbName, False)
    #two functions are now supported:
    #1. get_all_id: will return a list containing all user ids
    print simpleDataStore.get_all_id()

    #2. get_one_user: specify the user id, and will return the correponding data as a tuple. (see the print result)
    for userID in simpleDataStore.get_all_id():
        print simpleDataStore.get_one_user(userID)

    simpleDataStore.close()

if __name__ == '__main__':
    main()










