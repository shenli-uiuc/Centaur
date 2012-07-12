#!/usr/bin/python
# -*- coding: utf-8 -*-


from MySQLDataStore import MySQLDataStore
from GoogleGeo import GoogleGeo

class CoorCrawler:

    INFTY = 99999

    offset = 0
    filename = "loc_offset.txt"
    googleGeo = None
    dataStore = None

    def __init__(self):
        f = open(self.filename, 'r')
        self.offset = int(f.readline())
        f.close()
        self.googleGeo = GoogleGeo()
        self.dataStore = MySQLDataStore()

    def get_address(self):
        cnt = self.dataStore.select_user_count()
        print ("count: ", cnt)
        while self.offset < cnt:
            self.offset += 1
            print ("offset: ", self.offset)
            f = open(self.filename, 'w')
            f.write("%d\n"%(self.offset))
            f.close()
            loc = self.dataStore.select_user_location_offset(self.offset)
            print loc
            if not loc:
                print ("in not loc")
                continue
            tmp = self.dataStore.select_addr_location(loc)
            if tmp:
                print ("in address", tmp)
                continue
            res = self.googleGeo.get_coordination(loc)
            if res:
                (lati, long, formatted, types) = res
            else:
                lati = -self.INFTY
                long = -self.INFTY
                formatted = None
                types = "None"

            print  (loc, lati, long, formatted, types)
            self.dataStore.insert_address(loc, lati, long, formatted, types)
             
                


def main():
    coorCrawler = CoorCrawler()
    coorCrawler.get_address()

if __name__ == "__main__":
    main()
