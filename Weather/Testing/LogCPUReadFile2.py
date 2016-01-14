
#!/usr/bin/python
#--------------------------------------
# Modified to  as simple as possible
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
THINGSPEAKKEY	= 'APIKEY'
THINGSPEAKURL	= 'api.thingspeak.com'
INTERVAL		= 1    # Delay between each reading (mins)
CFGFILE			= '/home/pi/Weather/templogger.cfg'
DATAFILE		= '/home/pi/Weather/LastReadingPWWS.txt'
TEMPOUT			= 1
AIRPRESSURE		= 2

#####################################################


def readDataFile():
	# NOT FINISHED
	
	#sudo python -m pywws.Template /home/pi/Weather/WS/data ~/home/pi/Weather/WS/templates_used/tweet.txt /home/pi/Weather/WS/results/tweet.txt
	#cat /home/pi/Weather/WS/results/tweet.txt

	if os.path.isfile(DATAFILE)==True:
		print "Found data file"
		f = open(DATAFILE,'r')
		data = f.read().splitlines()
		f.close()
		if data[0]=='Temp Logger':
			print "Using data file"
			TEMPOUT		= int(data[1])
			AIRPRESSURE	= int(data[2])	
		
def postToThingspeak():
	cpu_pc = psutil.cpu_percent()
	mem_avail_mb = psutil.net_io_counters()	
	params = urllib.urlencode({'field1': cpu_pc, 'field2': mem_avail_mb.packets_recv,'key':'33SZ0OIP50YU8809'})
	headers = {"Content-type": "application/x-www-form-urlencoded","Accept": "text/plain"}
	conn = httplib.HTTPConnection("api.thingspeak.com")
	
	try:
		conn.request("POST", "/update", params, headers)
		response = conn.getresponse()
		print "cpu_percent", cpu_pc
		print "packets_recv", mem_avail_mb.packets_recv
		print strftime("%a, %d %b %Y %H:%M:%S", localtime())
		print response.status, response.reason
		data = response.read()
		conn.close()
	except:
		print "connection failed"	
		
def postToThingspeak2():
	params = urllib.urlencode({'field1': TEMPOUT, 'field2': AIRPRESSURE,'key':THINGSPEAKKEY})
	headers = {"Content-type": "application/x-www-form-urlencoded","Accept": "text/plain"}
	conn = httplib.HTTPConnection(THINGSPEAKURL)
	
	try:
		conn.request("POST", "/update", params, headers)
		response = conn.getresponse()
		print strftime("%a, %d %b %Y %H:%M:%S", localtime()), " Temp Out:", TEMPOUT, " Air pressure:", AIRPRESSURE
		print "Post status: ", response.status, response.reason
		data = response.read()
		conn.close()
	except:
		print "EXCEPTION: Connection failed"			

def postToThingspeak3(thingspeakkey,thingspeakurl,tempout,airpressure):
	params = urllib.urlencode({'field1': tempout, 'field2': airpressure,'key':thingspeakkey})
	headers = {"Content-type": "application/x-www-form-urlencoded","Accept": "text/plain"}
	conn = httplib.HTTPConnection(thingspeakurl)
	
	try:
		conn.request("POST", "/update", params, headers)
		response = conn.getresponse()
		print strftime("%a, %d %b %Y %H:%M:%S", localtime()), " Temp Out:", tempout, " Air pressure:", AIRPRESSURE
		print "Post status: ", response.status, response.reason
		data = response.read()
		conn.close()
	except:
		print "EXCEPTION: Connection failed"
		
def sendDataERIK(url,key,field1,field2,temp,pres):
  # NOT FINISHED
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
	global INTERVAL
	global CFGFILE
	global DATAFILE
	global TEMPOUT
	global AIRPRESSURE
	
	print 'start read...'
	print 'url=', THINGSPEAKURL
	print 'cfgfile=', CFGFILE
	if os.path.isfile(CFGFILE)==True:
		print "Found templogger.cfg"
		f = open(CFGFILE,'r')
		data = f.read().splitlines()
		f.close()
		if data[0]=='Temp Logger':
			print "Using templogger.cfg"
			THINGSPEAKKEY	= data[1]
			THINGSPEAKURL	= data[2]
			INTERVAL		= int(data[3])
			CFGFILE			= data[4]
			DATAFILE		= data[5]
			TEMPOUT			= int(data[6])
			AIRPRESSURE		= int(data[7])
	else:
		print 'Missing templogger.cfg'
	
	print 'start Try'
	try:
		print 'inside try'
		#readConfigFile()
		print 'Did readConfigFile'
		while True:
			#readDataFile()
			print 'Did readDataFile'
			#postToThingspeak2()
			postToThingspeak3(THINGSPEAKKEY,THINGSPEAKURL,TEMPOUT,AIRPRESSURE)
			print 'Did postToThingspeak3'
			# DO NOT WORK PROPERLY ... sendDataERIK(THINGSPEAKURL,THINGSPEAKKEY,'field1','field2',TEMPOUT,AIRPRESSURE)
			sys.stdout.flush()
		
			# Toggle LED while we wait for next reading
			for i in range(0,INTERVAL*60):
				time.sleep(1)
			
			print "END"

	except :
		# Reset GPIO settings
		# GPIO.cleanup()
		print 'EXCEPTION: Cleanup.'

if __name__=="__main__":
	main()

