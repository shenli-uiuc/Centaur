#!/usr/bin/python
# -*- coding: utf-8 -*-


from MySQLDataStore import MySQLDataStore
from GoogleGeo import GoogleGeo

class CoorCrawler:

    INFTY = 99999

    filename = "prev_loc.txt"
    googleGeo = None
    dataStore = None
    loc = None

    def __init__(self):
        f = open(self.filename, 'r')
        self.loc = ''.join(f.readlines())
        f.close()
        self.googleGeo = GoogleGeo()
        self.dataStore = MySQLDataStore()

    def get_address(self):
        #cnt = self.dataStore.select_user_count()
        #print ("count: ", cnt)
        while True:
            f = open(self.filename, 'w')
            f.write(self.loc)
            f.close()
            self.loc = self.dataStore.select_user_location_offset(self.loc)
            print 
            if not self.loc:
                print ("in not loc")
                print ("done with current locations")
                break
            tmp = self.dataStore.select_addr_location(self.loc)
            if tmp:
                print ("in address", tmp)
                continue
            res = self.googleGeo.get_coordination(self.loc)
            if res:
                (lati, long, formatted, types) = res
            else:
                lati = -self.INFTY
                long = -self.INFTY
                formatted = None
                types = "None"

            print  (self.loc, lati, long, formatted, types)
            self.dataStore.insert_address(self.loc, lati, long, formatted, types)
             
                


def main():
    coorCrawler = CoorCrawler()
    coorCrawler.get_address()

if __name__ == "__main__":
    main()
