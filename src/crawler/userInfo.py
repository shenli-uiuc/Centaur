import re
import urllib2
import simplejson as json

def getScreenName():
    inputFile = open("input.txt","r")
    outputFile = open("ScreenName.txt","w")
    for line in inputFile:
        name = re.split(r'[()]',line)
        outputFile.write(name[1]+'\n')
   
    inputFile.close()
    outputFile.close()

def getUserID():
    inputFile = open("ScreenName.txt","r")
    outputFile = open("UserIDs.txt","w")
    prefix="https://api.twitter.com/1/followers/ids.json?cursor=-1&screen_name="
    for line in inputFile:
        url = (prefix + line)[:-1]
        req = urllib2.urlopen(url)
        #print json.loads(req.read())
    
    req.close()
    inputFile.close()
    outputFile.close()
    
