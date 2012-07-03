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

    def get_coordination(self, strLoc):
        strLoc = self._loc_validate(strLoc)
        url = self.urlGeoCode%(strLoc)
        strData = urllib2.urlopen(url)
        data = json.loads(strData.read())
        if not data['status'] == 'OK':
            return None
        else:
            latitude = data['results'][0]['geometry']['location']['lat']
            longitude = data['results'][0]['geometry']['location']['lng']
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


if __name__=='__main__':
    main()
