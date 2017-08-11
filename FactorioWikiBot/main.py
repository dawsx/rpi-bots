#!/usr/bin/env python3

import creds
import praw
import urllib
import re
import time

def main():
	reddit = praw.Reddit(
		client_id = key,
		client_secret = secret,
		username = uname,
		password = passwd,
		user_agent = agent
	)
	subreddit = reddit.subreddit('factorio')

	for comment in subreddit.stream.comments():
		com = comment.body
		m = re.search("fact",com,re.I)
		if m:
			for c in com:
				try:
					print(c, end="")
				except:
					print("#", end="")
					
			print("\n----------------")
		time.sleep(2)
main()