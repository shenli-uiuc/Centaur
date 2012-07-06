import urllib2
import time

from RateLimit import RateLimit

class URLHandler:

    sleepTime = 5
    rateLimitError = 400
    
    rateLimit = None

    def __init__(self):
        self.rateLimit = RateLimit()

    def open_url(self,url):
        count = 1
        while (count):
            if (count == 10):
                print ("In URLHandler.open_url: URL Exception Occur", url)
                return None
            try:
                self.rateLimit.check()
                res = urllib2.urlopen(url)
                print (url, count)
                return res
            except urllib2.HTTPError, e:
                print ("In URLHandler.open_url: ", e.code, e.strerror, e.message)
                if self.rateLimitError == e.code:
                    self.rateLimit.check()    
                count = count + 1
                time.sleep(self.sleepTime)
            except urllib2.URLError, e:
                print ("In uRLHandler.open_url: ", e.reason)
                count = count + 1
                time.sleep(self.sleepTime)
