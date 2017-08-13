#!/usr/bin/env python3

import creds
import praw
import urllib
import re
import time
import wiki

oldcomments = "oldcomments"
sig = "^^I ^^am ^^a ^^bot, ^^beep ^^boop ^^| ^^Source ^^| ^^Created ^^by ^^u/thisisdada"
try:
	f = open(oldcomments, 'r')
	f.close()
except:
	f = open(oldcomments, 'w')
	f.close()
	
base = 'https://wiki.factorio.com/api.php?'

def main():
	reddit = praw.Reddit(
		client_id = creds.key,
		client_secret = creds.secret,
		username = creds.uname,
		password = creds.passwd,
		user_agent = creds.agent
	)
	subreddit = reddit.subreddit('justasandboxforbots')

	for comment in subreddit.stream.comments():
		com = comment.body
		print (com)
		matches = re.finditer("linkwiki:([^\n]+)",com,re.I)
		topics = []
		for m in matches:
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
					
			if numhits != 0:
				comstr = ""
				for i in range(len(outstrs)):
					if outstrs[i] != -1:
						comstr += outstrs[i]
					else:
						comstr += "I'm sorry, I didn't find a page titled \"{}\".\n\n".format(topics[i])
						comstr += "*****\n\n"
			
				print (comstr)
		time.sleep(2)
main()