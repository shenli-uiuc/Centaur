import urllib2

class URLHandler:
    def open_url(self,url):
        count = 1
        while (count):
            if (count == 10):
                print "In URLHandler.open_url: URL Exception Occur"
                return None
            try:
                res = urllib2.urlopen(url)
                return res
            except urllib2.HTTPError, e:
                print (e.strerror, e.message)
                count = count + 1
                time.sleep(5)
            except urllib2.URLError, e:
                print e.reason
                count = count + 1
                time.sleep(5)
