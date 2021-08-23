#!/usr/bin/python
import requests
import argparse
import csv
import os
from datetime import date
from bs4 import BeautifulSoup
from terminaltables import AsciiTable
from progress.spinner import Spinner
import math  

programData=[]
programData.append(['Name','URL','Bugs rewarded','Avg Resp Time','Avg Payout'])

def print_table():
	#os.system('cls' if os.name == 'nt' else 'clear')
	table = AsciiTable(programData)
	#print(table.table)
	with open('bugcrowd-'+str(date.today())+'.csv','w') as outfile:
		wr= csv.writer(outfile,quoting=csv.QUOTE_ALL)
		wr.writerows(programData)
	exit()

def fetch_stats(url,cookie):
	bugscount=0
	avgresp='N/A'
	avgbounty='Zero'
	page = requests.get(url,cookies=cookie)
	soup = BeautifulSoup(page.text,"lxml")
	statsdiv=soup.findAll("p", { "class" : "stat" })

	bugscount=statsdiv[0].find('strong').text
	if len(statsdiv)>1:
		avgresp=statsdiv[1].find('strong').text
		if avgresp.startswith('$'):
			avgresp = 'N/A'
			avgbounty = statsdiv[1].find('strong').text
	if len(statsdiv)>2:
		avgbounty=statsdiv[2].find('strong').text
	avgbounty=avgbounty.replace(',','')
	print(bugscount, avgresp, avgbounty)
	return bugscount, avgresp, avgbounty


def main():
	parser = argparse.ArgumentParser()
	parser.add_argument('--session',dest='session',default='',required=False,help='Enter your Bugcrowd _crowdcontrol_session cookie value for fetching private programs data')
	args = parser.parse_args()
	count = 0
	#urlx = "https://bugcrowd.com/programs?page="
	url = "https://bugcrowd.com/programs.json?"
	
	cookie={'_crowdcontrol_session':args.session} 
	
	response = requests.get(url,cookies=cookie)
	response_json = response.json()
	program_count = int(response_json["meta"]["totalHits"])
	pages = math.ceil(program_count/25)+1

	for i in range (1,pages):
		programs = response_json["programs"]
		for prog in programs:
			# print(prog)
			if (prog["accept_invitation_path"] or prog["program_url"].startswith("/programs/teasers")):
				continue
		
			prog_url="https://bugcrowd.com"+prog["program_url"]
			print(prog_url)
			name=prog["name"]
			
			bugcount,avgresp,avgbounty=fetch_stats(prog_url,cookie)
			programData.append([name,prog_url,bugcount,avgresp,avgbounty])

		offset = i * 25
		next_page = url+"offset%5B%5D="+str(offset)
		response = requests.get(next_page,cookies=cookie)
		response_json = response.json()

	print("All data fetched")
	print_table()

			
	# spinner = Spinner('Loading ')
	# while 1:
	# 	count = count+1
	# 	url = urlx+str(count)
	# 	cookie={'_crowdcontrol_session':args.session}
	# 	page = requests.get(url,cookies=cookie)
	# 	soup = BeautifulSoup(page.text,"lxml")
	# 	empty = soup.findAll("div", { "class" : "bc-blankstate" })    #This is when there are no programs.
	# 	if len(empty) == 1:
	# 		print_table()
	# 	else:
	# 		mydivs = soup.findAll("h4", { "class" : "bc-panel__title" })
	# 		for program in mydivs:
	# 			spinner.next()
	# 			try:
	# 				name = (program.find('a').text).encode('utf-8')
	# 				#print name
	# 				href = program.find('a')['href']
	# 				url = 'https://bugcrowd.com'+href
	# 				#print url
	# 				bugcount,avgresp,avgbounty=fetch_stats(url,cookie)
	# 				programData.append([name.encode('utf-8'),url.encode('utf-8'),bugcount.encode('utf-8'),avgresp.encode('utf-8'),avgbounty.encode('utf-8')])
	# 			except Exception as e:
	# 				pass


if __name__ == '__main__':
	main()
