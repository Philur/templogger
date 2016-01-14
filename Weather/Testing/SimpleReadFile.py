#!/usr/bin/python
#--------------------------------------
# Modified to  as simple as possible
#--------------------------------------
#import smbus
import time
import os
import sys
import urllib            # URL functions
import urllib2           # URL functions

import RPi.GPIO as GPIO  # GPIO library

################# Default Constants #################
# These can be changed if required
THINGSPEAKKEY	= '33SZ0OIP50YU8809'
THINGSPEAKURL	= 'api.thingspeak.com/update'
INTERVAL		= 1    # Delay between each reading (mins)
CFGFILE			= '/home/pi/Weather/templogger.cfg'
TEMPOUT			= 1
AIRPRESSURE		= 2

#####################################################

def readDataERIK():

  if os.path.isfile(CFGFILE)==True:
    print "Found templogger.cfg"
    f = open(CFGFILE,'r')
    data = f.read().splitlines()
    f.close()
    if data[0]=='Temp Logger':
	print "Using templogger.cfg"
	TEMPOUT = int(data[1])
	AIRPRESSURE = int(data[2])

def sendDataERIK(url,key,field1,field2,temp,pres):
  values = {'key' : key,'field1' : temp,'field2' : pres}

  postdata = urllib.urlencode(values)
  req = urllib2.Request(url, postdata)

  log = time.strftime("%d-%m-%Y,%H:%M:%S") + ","
  log = log + "{:.1f}C".format(temp) + ","
  log = log + "{:.2f}mBar".format(pres) + ","

  try:
    # Send data to Thingspeak
    response = urllib2.urlopen(req, None, 5)
    html_string = response.read()
    response.close()
    log = log + 'Update ' + html_string

  except urllib2.HTTPError, e:
    log = log + 'Server could not fulfill the request. Error code: ' + e.code
  except urllib2.URLError, e:
    log = log + 'Failed to reach server. Reason: ' + e.reason
  except:
    log = log + 'Unknown error'

  print log	  

def main():

  global THINGSPEAKKEY
  global THINGSPEAKURL
  global CFGFILE
  global TEMPOUT
  global AIRPRESSURE

  try:

    while True:
	readDataERIK()
	sendDataERIK(THINGSPEAKURL,THINGSPEAKKEY,'field1','field2',TEMPOUT,AIRPRESSURE)
	sys.stdout.flush()

 	# Toggle LED while we wait for next reading
	for i in range(0,INTERVAL*60):
		time.sleep(1)

  except :
	# Reset GPIO settings
	# GPIO.cleanup()
	sys.stdout('exception!')
  
if __name__=="__main__":
	main()
		

