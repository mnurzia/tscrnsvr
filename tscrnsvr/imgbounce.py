#!/usr/bin/env python3
import random
import time
import curses
import argparse
import sys
from tscrnsvr.shared import ScreenSpace, print_error, ColorObj
try:
	from PIL import Image
except:
	print_error("WARNING: The imgbounce module requires Pillow!")

__VERSION__ = "v0.1.1"

# imgbounce.py
# Bounce image screensaver.
# by illinoisjackson: https://github.com/illinoisjackson

if sys.version_info <= (3,0):
	_PY2 = 1
else:
	_PY2 = 0

class ImgBounceText:
	def __init__(self,win,img,args):
		self.win	= win
		self.pos 	= [10,10]
		self.co  	= ColorObj()
		self.colmap = []
		self.size 	= [int(c) for c in args.dimensions.split("x")]
		self.bbsize = self.size
		try:
			self.img = Image.open(img)
			self.img = self.img.convert("RGB")
			self.img = self.img.resize(self.size)
		except:
			print_error("IMGBOUNCE ERROR: Could not load image!")
			sys.exit(2)
		self.motion = [random.choice([-1,1]),random.choice([-1,1])]
		for y in range(self.size[1]):
			for x in range(self.size[0]):
				pc = self.img.getpixel((x,y))
				apxc = self.co.approxColor(pc)
				self.colmap.append(apxc)
	def render(self,screenspace):
		for y in range(self.size[1]):
			for x in range(self.size[0]):
				screenspace.addchar(self.pos[0]+(x*2),self.pos[1]+y,ord("█"),self.colmap[(y*self.size[1])+x])
				screenspace.addchar(self.pos[0]+(x*2)-1,self.pos[1]+y,ord("█"),self.colmap[(y*self.size[1])+x])
		for xu in range(self.pos[0]-1, \
						self.pos[0]+(self.size[0])*2+1):
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
	bt	 = ImgBounceText(stdscr,args.image,args)
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
				deb.append("%s\tframes, delay %s, image %s" % (str(TICK),str(args.delay),args.image))
			SCSP.render(debug=deb,ref=False,clear=False)
			time.sleep(args.delay)
			if args.screensaver:
				if SCSP.win.getch() != -1:
					SCSP.destroy()
					sys.exit()
			else:
				if SCSP.win.getch() == ord("q"):
					SCSP.destroy()
					sys.exit()
			SCSP.win.erase()
			TICK += 1
	except KeyboardInterrupt:
		SCSP.destroy()
		sys.exit()

def get_args():
	return [
			"imgbounce",
			"Bounce an image around your terminal.",
			
			[(("-d", "--delay"), {"type":float, "default":0.1,
				"help":"set delay between frames in seconds (default 0.1)"}),
			
			(("-g", "--debug"), {"action":"store_true",
				"help":"show debug statistics in upper left corner"}),
			
			(("-s", "--screensaver"), {"action":"store_true",
				"help":"screensaver mode (press any key to leave)"}),
				
			(("-x", "--dimensions"), {"type":str, "default":"32x32",
				"help":"dimensions for image to bounce (default 32x32)"}),
			
			(["image"], {"type":str,
				"help":"set image for bounce"})]
			]

def run(args):
	curses.wrapper(main,args)
		