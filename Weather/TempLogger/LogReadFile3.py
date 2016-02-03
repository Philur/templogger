#!/usr/bin/python
#--------------------------------------
# Modified to  as simple as possible
# LogReadFile2.py
#--------------------------------------
import httplib
from time import localtime, strftime
import psutil

#import smbus
import time
import os
import sys
import urllib            # URL functions
import urllib2           # URL functions

import RPi.GPIO as GPIO  # GPIO library

################# Default Constants #################
# These can be changed if required
CFGFILE			= '/home/pi/Weather/templogger.cfg'		# Path to config file. This parameter must be set correctly and do not need to be read from file
THINGSPEAKKEY	= 'APIKEY'		# API key for thingspeak.com
THINGSPEAKURL	= 'url'			#'api.thingspeak.com'
INTERVAL		= 1				# Delay between each reading (mins)
DATAFILE		= 'datafile'	# Path to data file i.e. '/home/pi/Weather/LastReadingPWWS.txt'
TEMPOUT			= 0				# Temperature outside
TEMPIN			= 0				# Temperature inside
FEELS = 0 # Feels like outside
HUMIDOUT = 0 # Humidity outside
HUMIDIN = 0 # Humidity inside
PRESSURE = 0 # relative pressure
WINDAVE = 0 # Wind Average
WINDGUST = 0 # Wind Gust
WINDDIR = 0 # Wind direction (degrees)


#####################################################

def readConfigFile(): # OK
	#print 'Access function readCfgFile'
	global THINGSPEAKKEY
	global THINGSPEAKURL
	global INTERVAL
	global CFGFILE
	global DATAFILE

	if os.path.isfile(CFGFILE)==True:
		#print "Found Config file"
		f = open(CFGFILE,'r')
		data = f.read().splitlines()
		f.close()
		if data[0]=='Temp Logger':
			#print "Using config data"
			THINGSPEAKKEY	= data[1]
			THINGSPEAKURL	= data[2]
			INTERVAL		= int(data[3])
			DATAFILE		= data[4]
		else:
			print 'Error in Config file'
	else:
		print 'Missing Config file'

def readDataFile(): # OK
	#print 'Access function readDataFile'
	global DATAFILE
	global TEMPOUT
	global TEMPIN
	global FEELS
	global HUMIDOUT
	global HUMIDIN
	global PRESSURE
	global WINDAVE
	global WINDGUST
	global WINDDIR
	
	if os.path.isfile(DATAFILE)==True:
		#print "Found Data file"
		f = open(DATAFILE,'r')
		data = f.read().splitlines()
		f.close()
		if data[0]=='Temp Logger':
			#print "Using data"
			TEMPOUT	= float(data[1])
			TEMPIN	= float(data[2])
			FEELS = float(data[3])
			HUMIDOUT = float(data[4])
			HUMIDIN = float(data[5])
			PRESSURE = float(data[6])
			WINDAVE = float(data[7])
			WINDGUST = float(data[8])
			WINDDIR = float(data[9])
		else:
			print 'Error in Data file'
	else:
		print 'Missing Data file'			
		

def postToThingspeak(): #OK
	#print 'Access function postToThningspeak'
	global THINGSPEAKKEY
	global THINGSPEAKURL
	global TEMPOUT
	global TEMPIN
	global FEELS
	global HUMIDOUT
	global HUMIDIN
	global PRESSURE
	global WINDAVE
	global WINDGUST
	global WINDDIR

	params = urllib.urlencode({'field1': TEMPOUT, 'field2': TEMPIN, 'field3': FEELS, 'field4': HUMIDOUT, 'field5': HUMIDIN, 'field6': PRESSURE, 'field7': WINDAVE, 'field8': WINDGUST, 'key':THINGSPEAKKEY})
	headers = {"Content-type": "application/x-www-form-urlencoded","Accept": "text/plain"}
	conn = httplib.HTTPConnection(THINGSPEAKURL)
	
	try:
		conn.request("POST", "/update", params, headers)
		response = conn.getresponse()
		print strftime("%a, %d %b %Y %H:%M:%S", localtime()), " Temp Out:", TEMPOUT, " Temp In:", TEMPIN, "Feels like: ", FEELS
		print "Post status: ", response.status, response.reason
		data = response.read()
		conn.close()
	except:
		print "EXCEPTION: Connection failed"			
		
def sendData(url,key,field1,field2,tempout,tempin): # NOT FINISHED. NOT USED YET
  values = {'key' : key,'field1' : tempout,'field2' : tempin}

  postdata = urllib.urlencode(values)
  req = urllib2.Request(url, postdata)

  log = time.strftime("%d-%m-%Y,%H:%M:%S") + ","
  log = log + "{:.1f}C".format(tempout) + ","
  log = log + "{:.2f}C".format(tempin) + ","

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
	global INTERVAL
	global CFGFILE
	global DATAFILE
	global TEMPOUT
	global TEMPIN
	global FEELS
	global HUMIDOUT
	global HUMIDIN
	global PRESSURE
	global WINDAVE
	global WINDGUST
	global WINDDIR
	
	#print 'start read...'
	#print 'url=', THINGSPEAKURL
	#print 'cfgfile=', CFGFILE
	
	#print 'start Try'
	try:
		#print 'inside try'
		readConfigFile()
		#print 'Did readConfigFile'
		cntLoop = int(0)
		while True:
			print "Loop: ", cntLoop
			cntLoop = cntLoop + 1
			
			readDataFile()
			#print 'Did readDataFile'
			postToThingspeak()
			#print 'Did postToThingspeak'
			#sendDataTHINGSPEAKURL,THINGSPEAKKEY,'field1','field2',TEMPOUT,TEMPIN)
			sys.stdout.flush()
		
			# Toggle LED while we wait for next reading
			for i in range(0,INTERVAL*60):
				time.sleep(1)

	except :
		# Reset GPIO settings
		# GPIO.cleanup()
		print 'EXCEPTION: Cleanup.'

if __name__=="__main__":
	main()
