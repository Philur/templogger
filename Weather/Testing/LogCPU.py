import httplib, urllib
from time import localtime, strftime
# download from http://code.google.com/p/psutil/
import psutil
import time

def doit():
	cpu_pc = psutil.cpu_percent()
	mem_avail_mb = psutil.net_io_counters()	
	params = urllib.urlencode({'field1': cpu_pc, 'field2': mem_avail_mb.packets_recv,'key':'33SZ0OIP50YU8809'})
	headers = {"Content-type": "application/x-www-form-urlencoded","Accept": "text/plain"}
	conn = httplib.HTTPConnection("api.thingspeak.com")
	
	try:
		conn.request("POST", "/update", params, headers)
		response = conn.getresponse()
		print cpu_pc
		print mem_avail_mb.packets_recv
		print strftime("%a, %d %b %Y %H:%M:%S", localtime())
		print response.status, response.reason
		data = response.read()
		conn.close()
	except:
		print "connection failed"	

#sleep for 16 seconds (api limit of 15 secs)
if __name__ == "__main__":
	while True:
		doit()
		time.sleep(20)
