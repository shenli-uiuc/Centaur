import urllib2
import sys

username = sys.stdin.readline() 
password = sys.stdin.readline()

username = username.split('\n')
username = username[0]
password = password.split('\n')
password = password[0]

print (username, password)

request = urllib2.Request( 'https://stream.twitter.com/1.1/statuses/sample.json' )
request.add_header( 'Authorization', 'Basic ' + base64.b64encode( username + ':' + password ) )
response = urllib2.urlopen( request )

CHUNK = 16 * 1024
with open(file, 'wb') as fp:

fp = open('/scratch/shenli3/data/sample-10-20', 'wb')
  while True:
    chunk = response.read(CHUNK)
    if not chunk: break
    fp.write(chunk)
