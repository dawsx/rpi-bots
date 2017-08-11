#!/usr/bin/env python3

import creds
import praw
import urllib
import re
import time

oldcomments = "oldcomments"
try:
	f = open(oldcomments, 'r')
	f.close()
except:
	f = open(oldcomments, 'w')
	f.close()

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
		matches = re.finditer("linkwiki: ([^\n]*)",com,re.I)
		for m in matches:
			topic = re.sub(r' ','_',"".join([x for x in m.group(1) if 31 < ord(x) < 127]))
			topic = re.sub(r'_*$', '', topic)
			
			# for c in com:
				# try:
					# print(c, end="")
				# except:
					# print("#", end="")
			print (topic)
			print("\n----------------")
		time.sleep(2)
main()