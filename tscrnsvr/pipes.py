#!/usr/bin/env python3
import random
import time
import sys
import curses
import argparse
import math
from tscrnsvr.shared import ScreenSpace

__VERSION__ = "v0.1"

# pipes.py
# Pipe screensaver 
# by illinoisjackson: https://github.com/illinoisjackson

if sys.version_info <= (3,0):
	_PY2 = 1
else:
	_PY2 = 0

PIPETYPES =	[
		"│╭X╮╯─╮XX╰│╯╰X╭─",
		"│┌X┐┘─┐XX└│┘└X┌─",
		"┃┏X┓┛━┓XX┗┃┛┗X┏━",
		"║╔X╗╝═╗XX╚║╝╚X╔═"
		]

class Pipe:
	def __init__(self,color,screenspace,style):
		self.color 	= int(color)
		self.dirch 	= [[0,-1],
						[1,0],
						[0,1],
						[-1,0]]
		self.dir	= random.randint(0,3)
		self.realdir= self.dirch[self.dir]
		self.pos	= [random.randint(0,screenspace.size[1]),random.randint(0,screenspace.size[0])]
		self.chars 	= style
	def render(self,screenspace):
		if random.random() <= 0.20:
			self.ldir = self.dir
			self.choose = True
			while True:
				self.dir = random.randint(0,3)
				if abs(self.dirch[self.dir][0]) != abs(self.dirch[self.ldir][0]):
					if abs(self.dirch[self.dir][1]) != abs(self.dirch[self.ldir][1]):
						break
			self.realdir = self.dirch[self.dir]
			self.char = self.chars[(self.ldir*4)+self.dir]
		else:
			self.char = self.chars[((self.dir)*5)]
		screenspace.addchar(self.pos[0] % screenspace.size[1],self.pos[1] % screenspace.size[0],ord(self.char),self.color)
		self.pos[0] += self.realdir[0]
		self.pos[1] += self.realdir[1]

def main(stdscr,args):
	SCSP = ScreenSpace(stdscr)
	PIPES = []
	STARTTIME = time.time()
	while True:
		TICK = 0
		for pp in range(0,args.pipes):
			PIPES.append(Pipe(random.choice(args.colors.split(",")),
						SCSP,
						PIPETYPES[args.style-1]))
		for fr in range(0,args.rstime):
			deb = []
			if (time.time()-STARTTIME) < 2:
				if not args.screensaver:
					deb.append("Press Q or CTRL-C to quit.")
				if _PY2:
					deb.append("NOTE: Colors do not work properly in python2.")
					deb.append("Try running in python3 to get colors working.")
			if args.debug == True:
				deb.append("pipes.py %s" % __VERSION__)
				deb.append("%s\tframes, delay %s, pipes %s" % (str(TICK),str(args.delay),args.pipes))
			if args.screensaver:
				if SCSP.win.getch() != -1:
					SCSP.destroy()
					sys.exit()
			else:
				if SCSP.win.getch() == ord("q"):
					SCSP.destroy()
					sys.exit()
			TICK += 1
			for pp in PIPES:
				pp.render(SCSP)
			SCSP.render(deb,clear=False)
			time.sleep(args.delay)
		PIPES = []
		SCSP.win.clear()

def get_args():
	return [
			"pipes",
			"Screensaver similar to that of Windows XP; only 2D.",
			
			[(("-d", "--delay"), {"type":float, "default":0.1,
				"help":"set delay between frames in seconds (default 0.1)"}),
			
			(("-n", "--pipes"), {"type":int, "default":10,
				"help":"set number of pipes on screen (default 10)"}),
			
			(("-c", "--colors"), {"type":str, "default":",".join([str(x) for x in range(0,256)]),
				"help":"set pipe colors. "+\
					"Must be a comma separated list of values on the terminal's color palette. "+\
					"(default random choice)"}),
			
			(("-C", "--style"), {"type":int, "default":3,
				"help":"set pipe style. Non-zero integer up to 4."}),
			
			(("-r", "--rstime"), {"type":int, "default":200,
				"help":"restart pipe system every RSTIME frames. (default 200)"}),
				
			(("-g", "--debug"), {"action":"store_true",
				"help":"show debug statistics in upper left corner"}),
			
			(("-s", "--screensaver"), {"action":"store_true",
				"help":"screensaver mode (press any key to leave)"})]
			]

def run(args):
	curses.wrapper(main,args)