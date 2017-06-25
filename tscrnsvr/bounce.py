#!/usr/bin/env python3
import random
import time
import curses
import argparse
import sys
from tscrnsvr.shared import ScreenSpace

__VERSION__ = "v0.1.1"

# bounce.py
# Bounce text screensaver.
# by illinoisjackson: https://github.com/illinoisjackson

if sys.version_info <= (3,0):
	_PY2 = 1
else:
	_PY2 = 0

class BounceText:
	def __init__(self,win,text,colors):
		self.win	= win
		self.pos = [10,10]
		self.text	= text
		self.colors = colors
		self.motion = [random.choice([-1,1]),random.choice([-1,1])]
		self.lln = 0
		for line in self.text.split("\n"):
			if len(line) > self.lln:
				self.lln = len(line)
		self.size = [self.lln,len(self.text.split("\n"))]
	def render(self,screenspace):
		for ln, line in enumerate(self.text.split("\n")):
			for cn, char in enumerate(line):
				screenspace.addchar(self.pos[0]+cn,self.pos[1]+ln,ord(char),self.colors)
		for xu in range(self.pos[0]-1, \
						self.pos[0]+self.size[0]+1):
			for yu in range(self.pos[1]-1, \
							self.pos[1]+self.size[1]+1):
				if xu < 0:
					self.motion[0] = 1
				if xu >= self.win.getmaxyx()[1]:
					self.motion[0] = -1
				if yu < 0:
					self.motion[1] = 1
				if yu >= self.win.getmaxyx()[0]:
					self.motion[1] = -1
		self.pos[0] += self.motion[0]
		self.pos[1] += self.motion[1]
	
def main(stdscr,args):
	STARTTIME = time.time()
	TICK = 0
	SCSP = ScreenSpace(stdscr)
	bt	 = BounceText(stdscr,args.string,args.color)
	try:
		while True:
			bt.render(SCSP)
			deb = []
			if (time.time()-STARTTIME) < 2:
				if not args.screensaver:
					deb.append("Press Q or CTRL-C to quit.")
				if _PY2:
					deb.append("NOTE: Colors do not work properly in python2.")
					deb.append("Try running in python3 to get colors working.")
			if args.debug == True:
				deb.append("bounce.py %s" % __VERSION__)
				deb.append("%s\tframes, delay %s, color %s" % (str(TICK),str(args.delay),args.color))
			SCSP.render(debug=deb)
			time.sleep(args.delay)
			if args.screensaver:
				if SCSP.win.getch() != -1:
					SCSP.destroy()
					sys.exit()
			else:
				if SCSP.win.getch() == ord("q"):
					SCSP.destroy()
					sys.exit()
			TICK += 1
	except KeyboardInterrupt:
		SCSP.destroy()
		sys.exit()

def get_args():
	return [
			"bounce",
			"Bounce text around your terminal.",
			[(("-d", "--delay"), {"type":float, "default":0.1,
				"help":"set delay between frames in seconds (default 0.1)"}),
			
			(("-c", "--color"), {"type":int, "default":15,
				"help":"set color of text (default 15)"}),
			
			(("-g", "--debug"), {"action":"store_true",
				"help":"show debug statistics in upper left corner"}),
			
			(("-s", "--screensaver"), {"action":"store_true",
				"help":"screensaver mode (press any key to leave)"}),
			
			(("-S", "--string"), {"type":str, "default":"test",
				"help":"set string for bounce"})]
			]

def run(args):
	curses.wrapper(main,args)
		