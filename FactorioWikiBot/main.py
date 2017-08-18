#!/usr/bin/env python3

import creds
import praw
import urllib
import re
import time
import wiki
import logging
import atexit

logfile = "logs/fwikibot.log"
FORMAT = '%(asctime)-15s, %(filename)s:%(levelname)s: %(message)s'
logging.basicConfig(filename = logfile, level = logging.DEBUG, format = FORMAT)
logging.info('Initializing bot...')

oldcomments = "oldcomments"
sig = "^^I ^^am ^^a ^^bot, ^^beep ^^boop ^^| [^^Source](https://github.com/"
sig += "dawsx/rpi-bots/tree/master/FactorioWikiBot) ^^| ^^Created ^^by ^^u/"
sig += "thisisdada"
currcomment = ""

try:
	f = open(oldcomments, 'r')
	f.close()
except:
	f = open(oldcomments, 'w')
	f.close()
	
base = 'https://wiki.factorio.com/api.php?'

def exitfunc():
	logging.info("Bot has shut down while processing comment {}".format(currcomment))
	
atexit.register(exitfunc)

def main():
	reddit = praw.Reddit(
		client_id = creds.key,
		client_secret = creds.secret,
		username = creds.uname,
		password = creds.passwd,
		user_agent = creds.agent
	)
	subreddit = reddit.subreddit('factorio')

	for comment in subreddit.stream.comments():
		time.sleep(2)
		comlist = []
		with open(oldcomments, 'r') as f:
			comdata = f.read()
			comlist = comdata.split("\n")
		com = comment.body
		comid = comment.id
		currcomment = comid
		logging.info("Processing comment {}".format(comid))
		if comid in set(comlist):
			logging.debug(
				"Already processed comment {}, skipping...".format(comid))
			continue
		cauth = comment.author
		if cauth.name == creds.uname:
			logging.debug(
				"Skipping comment with author {}...".format(cauth.name))
		else:
			#print(comid)
			comstr = ""
			#print (com)
			matches = re.finditer("linkwiki:([^\n]+)",com,re.I)
			topics = []
			for m in matches:
				logging.debug(
					"Found match on comment {}: \"{}\"".format(comid, m))
				topic = "".join([x for x in m.group(1) if 31 < ord(x) < 127])
				topic = re.sub(r' *$', '', topic)
				topic = re.sub(r'^ *', '', topic)
				topics.append(topic)
				
			if len(topics) > 0:
				numhits = 0
				outstrs = []
				for t in topics:
					hitstring = wiki.query(t)
					outstrs.append(hitstring)
					if hitstring != -1:
						numhits += 1
						logging.info("Query for \"{}\" successful".format(t))
					else:
						logging.info("Query for \"{}\" unsuccessful".format(t))
						
				if numhits != 0:
					comstr = ""
					for i in range(len(outstrs)):
						if outstrs[i] != -1:
							comstr += outstrs[i]
						else:
							comstr += "> I'm sorry, I didn't find a page titled"
							comstr += " \"{}\".\n\n".format(topics[i])
							comstr += "*****\n\n"
				
					#print (comstr + sig)
					comment.reply(comstr + sig)
					logging.info("Replied to comment {}".format(comid))
					
		
		comlist.append(comid)
		with open(oldcomments, 'w') as f:
			for c in comlist:
				if c != "":
					f.write(c + "\n")
main()