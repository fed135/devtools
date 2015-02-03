'''

#-------------------------------------------------------------------#

Image Optimizer

This software crawls through the provided media folder and sends
every png and jpg it finds to the tinyPNG/tinyJPG API.

Copyright 2014

#-------------------------------------------------------------------#

'''

#-----------#
#  Imports	#
#-----------#

import os, sys
from os.path import dirname
from urllib2 import Request, urlopen
from base64 import b64encode
from datetime import datetime

#-----------#
# Variables	#
#-----------#

TOTAL_FILES = 0
TOTAL_SAVED = 0

ACCEPTED_FILES = ['.png', '.PNG', '.jpg', '.JPEG', '.JPG', '.jpeg'] #perhaps exessive, we'll see

API_KEY = 'X9ioXjDy63-BRspyK78UFwRrfDO-W1D4' #Frederic's free trial key
API_URL = 'https://api.tinypng.com/shrink'
API_CERT = None
# Uncomment below if you have trouble validating our SSL certificate.
# Download cacert.pem from: http://curl.haxx.se/ca/cacert.pem
# cafile = dirname(__file__) + "/cacert.pem"

#-----------#
#  Classes	#
#-----------#

#CLI Color codes
class Colors:
    PATH = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'

#-----------#
#  Methods	#
#-----------#

#Walks in the media directory, looking for .png and .jpg files.
def collect_images(dir):

    global TOTAL_FILES

    for root, dirs, files in os.walk(dir):
        path = root.split('/')      
        for file in files:
            for i in range(len(ACCEPTED_FILES)):
                if (ACCEPTED_FILES[i] in file):
                    optimize_image(os.path.join(root, file))
                    TOTAL_FILES += 1


#Checks filesize changes
def optimize_image(file):

    global TOTAL_SAVED
    tstart = datetime.now()
    prevsize = os.path.getsize(file)
    newsize = 0
    saved = 0
    tend = 0
    delta = 0

    print 'optimizing ' + Colors.PATH + file + Colors.ENDC
    send_request(file)

    newsize = os.path.getsize(file)
    tend = datetime.now()
    delta = tend - tstart
    print '  process completed in ' + str(int(delta.total_seconds() * 1000)) + 'ms'

    saved = prevsize - newsize
    TOTAL_SAVED += saved
    if(saved < 0):
        print '  ' + str(prevsize) + ' --> ' + str(newsize) + Colors.WARNING + ' (+' + str(get_percent(prevsize, saved)) + '%)' +Colors.ENDC
    else:
        print '  ' + str(prevsize) + ' --> ' + str(newsize) + Colors.GREEN + ' (-' + str(get_percent(prevsize, saved)) + '%)' +Colors.ENDC
    print ''


#Calculates percentage gains or lost
def get_percent(original, saved):

    ori = int(original) + 0.0
    opt = int(saved) + 0.0
    hundred = 100.0

    if(opt < 0):
        return round(((opt*-1)/ori)*hundred, 2)
    else:
        return round((opt/ori)*hundred, 2)


#Sends the image optimization request
def send_request(url):

    request = Request(API_URL, open(url, 'rb').read())
    auth = b64encode(bytes('api:' + API_KEY)).decode('ascii')
    request.add_header('Authorization', 'Basic %s' % auth)
    handle_response(url, urlopen(request))


#Handles the optimization request response
def handle_response(url, response):

    if response.getcode() == 201:
    	headers = response.info().headers
    	for i in range(len(headers)):
    	    if ('Location: ' in headers[i]):
    	        remote = headers[i][10:].strip()
                save_to_disk(url, remote)
    else:
        print Colors.FAIL +' Error loading '+ url+Colors.ENDC
    response.close()


#Saves the response image to disk, overwriting the original one 
def save_to_disk(url, remote):

    result = urlopen(remote).read()
    open(url, "wb").write(result)


#Entry point
def welcome():

    print ''
    print '### IMAGE OPTIMIZATION ###'
    print '--------------------------'
    print ''
    collect_images(sys.argv[1])


#Wrap up
def goodbye():

	print '### COMPLETED ###'
	print '-----------------'
	print ''
	print 'Total files optimized: '+str(TOTAL_FILES)
	print 'Total bytes saved: '+str(TOTAL_SAVED) + Colors.ENDC

welcome()