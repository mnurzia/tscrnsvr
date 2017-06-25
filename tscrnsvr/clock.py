#!/usr/bin/env python3
import argparse
import curses
import time
import subprocess
import sys
from tscrnsvr.shared import ScreenSpace

__VERSION__ = "v0.1"

# clock.py
# clock screensaver 
# by illinoisjackson: https://github.com/illinoisjackson

if sys.version_info <= (3,0):
	_PY2 = 1
else:
	_PY2 = 0

def main(win,args):
	STARTTIME = time.time()
	TICK = 0
	SCSP = ScreenSpace(win)
	try:
		while True:
			formattedfigtime = time.strftime(args.topstrf)
			formattedsmalltime = time.strftime(args.bottomstrf)
			figtext = subprocess.check_output(["figlet","-f",args.font,formattedfigtime]).splitlines()
			ll = len(max(figtext, key=len))
			fh = len(figtext)
			sx = round((SCSP.size[1]-ll)/2)-1
			sy = round((SCSP.size[0]-fh)/2)
			for line,ln in enumerate(figtext):
				SCSP.addstr(sx,sy+line,ln,args.topcolor)
			SCSP.addstr(round((SCSP.size[1]-len(formattedsmalltime))/2),fh+1+sy,formattedsmalltime,args.bottomcolor)
			deb = []
			if (time.time()-STARTTIME) < 2:
				if not args.screensaver:
					deb.append("Press Q or CTRL-C to quit.")
				if _PY2:
					deb.append("NOTE: Colors do not work properly in python2.")
					deb.append("Try running in python3 to get colors working.")
			if args.debug == True:
				deb.append("clock.py %s" % __VERSION__)
				deb.append("%s\tframes" % (str(TICK)))
			SCSP.render(debug=deb,ref=False,clear=False)
			if args.screensaver:
				if SCSP.win.getch() != -1:
					SCSP.destroy()
					sys.exit()
			else:
				if SCSP.win.getch() == ord("q"):
					SCSP.destroy()
					sys.exit()
			SCSP.win.erase()
			time.sleep(0.1)
			TICK += 1
	except KeyboardInterrupt:
		sys.exit()

def get_args():
	return [
			"clock",
			"A simple digital clock. Requires FIGlet to be installed.",
			
			[(("-f", "--font"), {"type":str, "default":"banner",
				"help":"set FIGlet font that the digital clock should display (defaults to banner)"}),
				
			(("-tc", "--topcolor"), {"type":int, "default":0,
				"help":"set color for top text (default 15)"}),
			
			(("-bc", "--bottomcolor"), {"type":int, "default":0,
				"help":"set color for bottom text (default 15)"}),
			
			(("-ts", "--topstrf"), {"type":str, "default":"%I:%M:%S %p",
				"help":"string to be passed to time.strftime() for the top text (default \"%%I:%%M:%%S %%p\")"}),
			
			(("-bs", "--bottomstrf"), {"type":str, "default":"%A, %B %d, %Y",
				"help":"string to be passed to time.strftime() for the bottom text (default \"%%A, %%B %%d, %%Y\")"}),
			
			(("-g", "--debug"), {"action":"store_true",
				"help":"show debug statistics in upper left corner"}),
			
			(("-s", "--screensaver"), {"action":"store_true",
				"help":"run in screensaver mode (press any key to exit)"}),]]

def run(args):
	curses.wrapper(main,args)