import base64
import urllib2
import sys

username = sys.stdin.readline() 
password = sys.stdin.readline()

username = username.split('\n')
username = username[0]
password = password.split('\n')
password = password[0]

print (username, password)

request = urllib2.Request( 'https://stream.twitter.com/1.1/statuses/filter.json?track=twitter,google,facebook,ibm,microsoft,vmware,linkedin,amazon,oracle,hp,adobe,cisco,apple,youtube,zynga,yahoo,firefox,blog,us,tweet' )
request.add_header( 'Authorization', 'Basic ' + base64.b64encode( username + ':' + password ) )
CHUNK = 16 * 1024;

nameformat = '/scratch/shenli3/data/sample-10-21-%d'
cnt = 0
while True:
    filename = nameformat%(cnt)
    fp = open(filename, 'wb')
    response = urllib2.urlopen( request )
    
    try:
        while True:
            chunk = response.read(CHUNK)
            if not chunk: 
                break
            fp.write(chunk)
    except:
        pass
    fp.close()
    cnt += 1
