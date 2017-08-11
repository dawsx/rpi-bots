#!/usr/bin/env python3

import subprocess
import time
import os
import atexit

def cleanup(procs):
	for p in procs:
		p.terminate()
		
dirs = []
with os.scandir() as base:
	for entry in base:
		if entry.is_dir() and entry.name != ".git":
			dirs.append(entry.name)

procs = []
for d in dirs:
	try:
		p = subprocess.Popen(["python3", "{}/main.py".format(d)])
	except:
		print("No main.py in {}", d)
		
	procs.append(p)
	
atexit.register(cleanup(procs))