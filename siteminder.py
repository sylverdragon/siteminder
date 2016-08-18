# Siteminder - Simple python script for monitoring a web site.  Siteminder will monitor the specified site and send SMS alerts when 
# 		the site becomes unresponsive. 
import argparse
import requests
import time
from datetime import datetime

def main():
	parser = argparse.ArgumentParser()
	parser.add_argument('anum',type=str,help='Mobile number to receive SMS alerts')
	parser.add_argument('url',type=str,help='URL to scan')
	args = parser.parse_args()
	strPhone = args.anum
	strSite = args.url
	strMsg = '!!!DDaemon web monitor on ice-nine -- Site ** ' + strSite + ' ** down @ '
	strResMsg = '!!!DDaemon on ice-nine -- Site ** ' + strSite + ' ** on-line @ '
	iInterval=10
	bSend = True
	while True:
		try:
			requests.packages.urllib3.disable_warnings()
			res = requests.get(strSite,timeout=3,verify=False)
			if res.status_code == 200:
				if not bSend:
					errMsg = strResMsg + datetime.now().strftime("%Y-%m-%d %H:%M:%S %Z")
					params = {'number':strPhone, 'message':errMsg}
					res = requests.post("http://textbelt.com/text", data=params)
					print( errMsg)
					bSend = True
				else:
					print("No alert necessary - Site on-line @ " + datetime.now().strftime("%Y-%m-%d %H:%M:%S %Z"))
			else:
				print("No alert necessary - Site on-line @ " + datetime.now().strftime("%Y-%m-%d %H:%M:%S %Z"))
		except (requests.exceptions.Timeout, requests.exceptions.ConnectionError):
			if bSend:
				errMsg = strMsg + datetime.now().strftime("%Y-%m-%d %H:%M:%S %Z")
				params = {'number':strPhone, 'message':strMsg}
				res = requests.post("http://textbelt.com/text", data=params)
				print( errMsg)
				bSend = False
			else:
				print("Site down - Alert suppressed @ " + datetime.now().strftime("%Y-%m-%d %H:%M:%S %Z"))
				
		time.sleep(iInterval)
		
if __name__ == "__main__":
	main()

