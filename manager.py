#!/usr/bin/env python3

from tendo import singleton
me = singleton.SingleInstance()

import subprocess
import time
import os
import atexit

procs = []
def cleanup():
	for p in procs:
		p.terminate()

def initproc(d):	
	os.chdir(d)
	p = subprocess.Popen(["python3", "main.py"])
	os.chdir("..")
	return [p,d]

base = os.scandir()
for entry in base:
	if entry.is_dir() and os.path.is_file("/".join(entry.name, "main.py")):
		procs.append(initproc(entry.name))

# Waiting loop; every 30 seconds it checks if each of its subprocesses 
# is running. If it finds that one has stopped, it relaunches the process
while True:
	time.sleep(30)
	for p in procs:
		if p[0].poll() != None:
			procs.remove(p)
			procs.append(initproc(p[1]))
	
atexit.register(cleanup)