#!/usr/bin/env python3
import random
import time
import sys
import curses
import argparse
from tscrnsvr.shared import ScreenSpace, print_error, parse_chars

__VERSION__ = "v0.1.1"

# matrix.py
# A cool matrix effect for your terminal!
# Fully customizable, of course.
# by illinoisjackson: https://github.com/illinoisjackson

if sys.version_info <= (3,0):
	_PY2 = 1
else:
	_PY2 = 0

class Fade:
	def __init__(self,starttick,x,y,headcolor,colors,unics,length,lifetime,speed):
		self.st		= starttick 
		self.colors	= colors
		self.lcolors= len(self.colors)
		self.headcolor = headcolor
		self.unics	= unics
		self.length = length
		self.lt		= lifetime
		self.speed	= speed
		self.pos	= [x,y]
		self.time	= 0
		self.dstd	= 0
	def render(self,tick,screenspace):
		self.time += 1
		for i in range(self.length):
			if i == 0:
				self.pendingcolor = self.headcolor
			else:
				self.pendingcolor = self.colors[int((i/self.length)*self.lcolors)]
			self.pendingchar  = random.choice(self.unics)
			screenspace.addchar(self.pos[0],round(self.pos[1])-i,self.pendingchar, \
					self.pendingcolor)
		self.pos[1] += self.speed
		if self.time == round(self.lt):
			self.dstd = 1
	def destroy(self):
		self = None
		
def main(stdscr,params,chars):
	STARTTIME = time.time()
	PARAMS = params
	FADES	= [None for fd in range(PARAMS.fades)]
	TICK = 0
	SCSP = ScreenSpace(stdscr)
	for fade in range(PARAMS.fades):
		FADES[fade] = Fade(
				TICK,
				random.randint(0,SCSP.size[1]),
				random.randint(0,SCSP.size[0]),
				PARAMS.headcolor,
				[int(j) for j in PARAMS.colors.rstrip(",").split(",")],
				chars,
				random.randint(PARAMS.minlength,PARAMS.maxlength),
				random.uniform(PARAMS.minlifetime,PARAMS.maxlifetime),
				random.uniform(PARAMS.minspeed,PARAMS.maxspeed))
	try:
		while True:
			time.sleep(PARAMS.delay)
			for fade in range(PARAMS.fades):
				if FADES[fade].dstd == 1:
					FADES[fade] = Fade(
				TICK,
				random.randint(0,SCSP.size[1]),
				random.randint(0,SCSP.size[0]),
				PARAMS.headcolor,
				[int(j) for j in PARAMS.colors.rstrip(",").split(",")],
				chars,
				random.randint(PARAMS.minlength,PARAMS.maxlength),
				random.uniform(PARAMS.minlifetime,PARAMS.maxlifetime),
				random.uniform(PARAMS.minspeed,PARAMS.maxspeed))
			for fade in FADES:
				fade.render(TICK,SCSP)
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
				deb.append("matrix.py %s" % __VERSION__)
				deb.append("%s\tframes, delay %s, colors %s, fades %s" % (str(TICK),str(PARAMS.delay),PARAMS.colors,str(PARAMS.fades)))
			SCSP.render(deb)
			TICK += 1
	except KeyboardInterrupt:
		SCSP.destroy()
		sys.exit()

def get_args():
	return [
			"matrix",
			"A screensaver like the one in the movie \"The Matrix\"",
			
			[(("-d", "--delay"), {"type":float, "default":0.1,
				"help":"set delay between frames in seconds (default 0.1)"}),
			
			(("-n", "--fades"), {"type":int, "default":40,
				"help":"set number of \"fades\" on screen (default 25)"}),
			
			(("-miln", "--minlength"), {"type":int, "default":4,
				"help":"set minimum length of fades (default 4)"}),
			
			(("-mxln", "--maxlength"), {"type":int, "default":20,
				"help":"set maximum length of fades (default 20)"}),
			
			(("-mis", "--minspeed"), {"type":float, "default":0.5,
				"help":"set minimum speed of fades (default 0.5)"}),
			
			(("-mxs", "--maxspeed"), {"type":float, "default":2,
				"help":"set maximum speed of fades (default 2)"}),
			
			(("-milt", "--minlifetime"), {"type":int, "default":10,
				"help":"set minimum lifetime of fades (default 10)"}),
			
			(("-mxlt", "--maxlifetime"), {"type":int, "default":30,
				"help":"set maximum lifetime of fades (default 30)"}),
			
			(("-c", "--colors"), {"type":str, "default":"83,84,119,120",
				"help":"set fade colors.\n"+\
				"Must be a comma separated list of values on the terminal's color palette.\n"+\
				"(default 83,84,119,120)"}),
			
			(("-cc", "--headcolor"), {"type":int, "default":16,
				"help":"set color of the first character of every fade."}),
			
			(("-C", "--chars"), {"type":str, "default":"32-128",
				"help":"set fade characters. Is a comma separated list of unicode ranges.\n"+\
					"Can be one character or a range. [Example: -C 32-55,66,2605,2606,6785-8941]\n"+\
					"(default 32-128)"}),
			
			(("-g", "--debug"), {"action":"store_true",
				"help":"show debug statistics in upper left corner"}),
			
			(("-s", "--screensaver"), {"action":"store_true",
				"help":"screensaver mode (press any key to leave)"})],
			]

def run(args):
	chars = parse_chars(args.chars)
	curses.wrapper(main,args,chars)