import subprocess
import time
import os

dirs = []
with os.scandir() as base:
	for entry in base:
		if entry.is_dir():
			dirs.append(entry.name)
			
