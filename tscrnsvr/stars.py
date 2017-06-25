#!/usr/bin/env python3
import random
import time
import sys
import curses
import argparse
import math
from tscrnsvr.shared import ScreenSpace, print_error, get_center, parse_chars

__VERSION__ = "v0.1.0"

# stars.py
# Star screensaver.
# by illinoisjackson: https://github.com/illinoisjackson

if sys.version_info <= (3,0):
	_PY2 = 1
else:
	_PY2 = 0
	
class Star:
	def __init__(self, color, x, y, acceleration, direction, char):
		self.pos = [x,y]
		self.color = color
		self.acceleration = acceleration
		self.direction = direction
		self.dstd = False
		self.char = char
	def render(self,screenspace):
		screenspace.addchar(round(self.pos[0]),round(self.pos[1]),self.char,self.color)
		self.pos[0] += self.direction[0] * self.acceleration
		self.pos[1] += self.direction[1] * self.acceleration
		if not screenspace.in_bounds(self.pos[0],self.pos[1]):
			self.dstd = True
	def destroy(self):
		self = None

def main(stdscr, PARAMS, chars):
	SCSP = ScreenSpace(stdscr)
	STARTTIME = time.time()
	TICK = 0
	clist = [int(i) for i in PARAMS.colors.split(',')]
	stlist = []
	try:
		while True:
			if random.random() < PARAMS.chance:
				ang = random.randint(0,359)
				stlist.append(Star(random.choice(clist),*get_center(stdscr),PARAMS.acceleration,[math.cos(ang),math.sin(ang)],random.choice(chars)))
			for n, star in enumerate(stlist):
				if star.dstd:
					star.destroy()
					stlist.pop(n)
				else:
					star.render(SCSP)
			if PARAMS.screensaver:
				if SCSP.win.getch() != -1:
					SCSP.destroy()
					sys.exit()
			else:
				if SCSP.win.getch() == ord("q"):
					SCSP.destroy()
					sys.exit()
			deb = []
			if (time.time()-STARTTIME) < 2:
				if not PARAMS.screensaver:
					deb.append("Press Q or CTRL-C to quit.")
				if _PY2:
					deb.append("NOTE: Colors do not work properly in python2.")
					deb.append("Try running in python3 to get colors working.")
			if PARAMS.debug == True:
				deb.append("stars.py %s" % __VERSION__)
				deb.append("%s\tframes, delay %s, stars %s" % (str(TICK),str(PARAMS.delay),str(len(stlist))))
			SCSP.render(deb)
			TICK += 1
			time.sleep(PARAMS.delay)
	except KeyboardInterrupt:
		sys.exit()
	
def get_args():
	return [
			"stars",
			"Make \"stars\" fly across your screen.",

			[(("-d", "--delay"), {"type":float, "default":0.01,
				"help":"set delay between frames in seconds (default 0.01)"}),
				
			(("-q", "--chance"), {"type":float, "default":0.2,
				"help":"Chance for a star to spawn each frame (default 0.2)"}),
				
			(("-c", "--colors"), {"type":str, "default":"227",
				"help": "set star colors.\n"+\
				"Must be a comma separated list of values on the terminal's color palette.\n"+\
				"(default 227)"}),
			
			(("-C", "--chars"), {"type":str, "default":"42",
				"help":"set star characters. Is a comma separated list of unicode ranges.\n"+\
					"Can be one character or a range. [Example: -C 32-55,66,2605,2606,6785-8941]\n"+\
					"(default 42)"}),
					
			(("-a", "--acceleration"), {"type":float, "default":0.3,
				"help":"Acceleration rate of stars (default 0.3)"}),
			
			(("-g", "--debug"), {"action":"store_true",
				"help":"show debug statistics in upper left corner"}),
			
			(("-s", "--screensaver"), {"action":"store_true",
				"help":"screensaver mode (press any key to leave)"})],
			]

def run(args):
	chars = parse_chars(args.chars)
	curses.wrapper(main,args,chars)
