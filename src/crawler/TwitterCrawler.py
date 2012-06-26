import urllib2
import simplejson as json

class Crawler:

    #you can specify other parameters (as described in the Twitter API page, e.g., user_id)
    urlGetFollowerID = "https://api.twitter.com/1/followers/ids.json?cursor=%d&screen_name=%s"    

    def get_one_user(self, userID):
        pass

    def get_one_user_piece(self, screenName, cursor = -1):
        url = self.urlGetFollowerID%(cursor, screenName)
        res = urllib2.urlopen(url)
        strData = res.read()
        data = json.loads(strData)
        #data now is python dictionary (something like a hash table)
        #ids is a integer array, storing follower ids
        ids = data['ids']
        #this query is not returning all the ids. As it is explained on Twitter API page, it only returns 5000 ids. The nextCursor specifies where we should start in next query
        nextCursor = data['next_cursor']
        return (ids, nextCursor)        

def main():
    crawler = Crawler()
    #When querying only the first piece, no need to specify curosr, as I set the default value to -1.
    (ids, nextCursor) = crawler.get_one_user_piece('ladygaga')
    print ids[10]
    print ids[1000]
    print nextCursor
    #query the second piece of ladygaga follower ids
    (ids, nextCursor) = crawler.get_one_user_piece('ladygaga', cursor = nextCursor)
    print ids[10]
    print ids[1000]
    print nextCursor

if __name__=='__main__':
    main()
        
