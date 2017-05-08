from bs4 import BeautifulSoup
import urllib2
import cookielib
from getpass import getpass
import sys
import time
import click





def run():

		cric=urllib2.urlopen("http://www.cricbuzz.com")

		html=cric.read()

		soup=BeautifulSoup(html)

		scoreall=soup.find_all("div",class_="cb-ovr-flo")

		list=[]
		c=0

		for link in scoreall:
				if link.string!=None:
								c+=1
								if c<6:
										list.append(link.string)

		s=list[0]+"\n"+list[1]+"\n"+list[2]+"\n"+list[3]+"\n"+list[4]
		message=s
		message = "+".join(message.split(' '))

		url = 'http://site24.way2sms.com/Login1.action?'
		data = 'username=' + username + '&password=' + passwd + '&Submit=Sign+in'


		cj = cookielib.CookieJar()
		opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))

		opener.addheaders = [('User-Agent','Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.120 Safari/537.36')]

		try:
				usock = opener.open(url, data)
		except IOError:
				print("Error while logging in.")
				sys.exit(1)

		jession_id = str(cj).split('~')[1].split(' ')[0]
		send_sms_url = 'http://site24.way2sms.com/smstoss.action?'
		send_sms_data = 'ssaction=ss&Token=' + jession_id + '&mobile=' + number + '&message=' + message + '&msgLen=136'
		opener.addheaders = [('Referer', 'http://site25.way2sms.com/sendSMS?Token=' + jession_id)]

		try:
				sms_sent_page = opener.open(send_sms_url, send_sms_data)
		except IOError:
				print("Error while sending message")

		print("SMS has been sent.")

@click.command()

def cli():
		global username 
		username = str(input("Enter Username: "))
		global passwd 
		passwd  = getpass()
		global number 
		number = str(input("Enter Mobile number: "))
		while True:
				 run()
				 time.sleep(2*60)
