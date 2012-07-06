#!/usr/bin/python
# -*- coding: utf-8 -*-

try:
    import json
except ImportError, e:
    import simplejson as json

import urllib2

class GoogleGeo:
    locPrefix = 'ÜT'

    urlGeoCode = 'http://maps.googleapis.com/maps/api/geocode/json?address=%s&sensor=false'

    def is_str_coor(self, strLoc):
        try:
            items = strLoc.split(',')
            a = items[0]
            b = items[1]
            items = a.split(' ')
            latitude = float(items[len(items) - 1])
            items = b.split(' ')
            longitude = float(items[len(items) - 1])
            return (latitude, longitude)
        except:
            return None

    def get_coordination(self, strLoc):
        coor = self.is_str_coor(strLoc)
        if not coor:
            strLoc = self._loc_validate(strLoc)
            url = self.urlGeoCode%(strLoc)
            strData = urllib2.urlopen(url)
            data = json.loads(strData.read())
            if not data['status'] == 'OK':
                return None
            else:
                latitude = data['results'][0]['geometry']['location']['lat']
                longitude = data['results'][0]['geometry']['location']['lng']
                formartted = data['results'][0]['formatted_address']
                types = data['results'][0]['types']
                return (latitude, longitude)

    def _loc_validate(self, strLoc):
        strLoc = '+'.join(strLoc.split())
        return strLoc

def main():
    geo = GoogleGeo()
    print geo.get_coordination('Beijing')
    print geo.get_coordination('Macy_s')
    print geo.get_coordination('I_m in your head...')
    print geo.get_coordination('The place I mean to be')
    print geo.is_str_coor('39.917725,116.551951')
    print geo.is_str_coor('ÃœT: 19.167049,72.845301')

if __name__=='__main__':
    main()
