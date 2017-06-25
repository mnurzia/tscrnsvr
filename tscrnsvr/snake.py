#!/usr/bin/env python3
import curses
import time
import random
import sys
from tscrnsvr.shared import ScreenSpace, get_center

def wrap(point,size):
	return [point[0] % size[1], point[1] % size[0]]

class Snake:
	def __init__(self,win,args):
		self.pos = get_center(win)
		self.wsize = win.getmaxyx()
		self.dir = [0,1]
		self.length = args.startlength
		self.tailpos = []
		self.fruitpos = [random.randint(0,self.wsize[1]-1),
						random.randint(0,self.wsize[0]-1)]
		for g in range(1,self.length+1):
			tp = self.pos[:]
			tp[1] = tp[1] - g
			self.tailpos.append(tp)
	def turnleft(self):
		if self.dir[1] == 1:
			return [1,0]
		elif self.dir[1] == -1:
			return [-1,0]
		elif self.dir[0] == 1:
			return [0,-1]
		elif self.dir[0] == -1:
			return [0,1]
	def turnright(self):
		if self.dir[1] == 1:
			return [-1,0]
		elif self.dir[1] == -1:
			return [1,0]
		elif self.dir[0] == 1:
			return [0,1]
		elif self.dir[0] == -1:
			return [0,-1]
	def render(self,screenspace,args):
		wsp = wrap(self.pos,screenspace.win.getmaxyx())
		screenspace.addchar(wsp[0],wsp[1],args.char,args.color)
		for ch in self.tailpos:
			wch = wrap(ch,screenspace.win.getmaxyx())
			screenspace.addchar(wch[0],wch[1],args.char,args.color)
		screenspace.addchar(self.fruitpos[0],self.fruitpos[1],args.fruitchar,args.fruitcolor)
		if wrap(self.pos,screenspace.win.getmaxyx()) != self.fruitpos:
			del self.tailpos[-1]
		else:
			self.wsize = screenspace.win.getmaxyx()
			self.fruitpos = [random.randint(0,self.wsize[1]-1),
							random.randint(0,self.wsize[0]-1)]
		self.tailpos.insert(0,self.pos[:])
		self.pos[0] += self.dir[0]
		self.pos[1] += self.dir[1]
		if wrap(self.pos,screenspace.win.getmaxyx()) in self.tailpos:
			screenspace.destroy()
			sys.exit()
		
def main(win,args):
	SCSP = ScreenSpace(win)
	SNK = Snake(win,args)
	try:
		while True:
			SNK.render(SCSP,args)
			SCSP.render(clear=False,ref=False)
			gc = SCSP.win.getch()
			if gc in [ord("a"),curses.KEY_LEFT]:
				SNK.dir = SNK.turnleft()
			if gc in [ord("d"),curses.KEY_RIGHT]:
				SNK.dir = SNK.turnright()
			if gc == ord("q"):
				SCSP.destroy()
				sys.exit()
			SCSP.win.erase()
			time.sleep(args.delay)
	except KeyboardInterrupt:
		pass

def get_args():
	return [
			"snake",
			"Play snake!",
			
			[(("-C", "--char"), {"type":int, "default":64,
				"help":"set code of the character for the snake's head and body (default 64)"}),
				
			(("-c", "--color"), {"type":int, "default":209,
				"help":"set color for snake"}),
			
			(("-F", "--fruitchar"), {"type":int, "default":65,
				"help":"set character for fruit (default 65)"}),
			
			(("-f", "--fruitcolor"), {"type":int, "default":125,
				"help":"set color for fruit (default 125)"}),
			
			(("-l", "--startlength"), {"type":int, "default":5,
				"help":"set starting length of snake"}),
			
			(("-d", "--delay"), {"type":float, "default":0.1,
				"help":"delay between each frame (default 0.1)"}),
			
			]]

def run(args):
	curses.wrapper(main,args)