try:
    import json
except ImportError,e:
    import simplejson as json

import time
import urllib2

class RateLimit:

    logFile = None
    logFileName = 'rateLimit.log' 

    urlCheckLimit = "https://api.twitter.com/1/account/rate_limit_status.json"

    def __init__(self):
        self.logFile = open(self.logFileName, 'w')

    def _open_url_limit(self,url):
        count = 1
        while (count):
            if (count >= 10):
                self.logFile.write("Error in requesting: %s\n"%(url))
                self.clean_up()
                sys.exit()
            try:
                res = urllib2.urlopen(url)
                return res
            except urllib2.HTTPError, e:
                self.logFile.write(str(e.strerror, e.message))
                count = count + 1
                time.sleep(30)
            except urllib2.URLError,e:
                self.logFile.write(e.reason)
                count = count + 1
                time.sleep(30)

    def _check_limit(self):
        url = self.urlCheckLimit
        res = self._open_url_limit(url)
        data = json.loads(res.read())
        limit = data['remaining_hits']
        wakeup = data['reset_time_in_seconds']
        return (limit,wakeup)


    def check(self):
        (limit, wakeup) = self._check_limit()
        while limit <= 0:
            interval = max(0, wakeup - time.time()) + 30
            time.sleep(interval)
            (limit, wakeup) = self._check_limit()

    def close(self):
        if self.logFile:
            self.logFile.close()
        
