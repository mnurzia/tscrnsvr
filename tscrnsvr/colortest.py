#!/usr/bin/env python3
import curses

def colortest(stdscr):
	# http://stackoverflow.com/questions/18551558/how-to-use-terminal-color-palette-with-curses
	curses.start_color()
	curses.use_default_colors()
	stdscr.addstr(0,0,"%s colors on \"%s\"\n" % (str(curses.COLORS),str(curses.termname().decode('ascii'))))
	for i in range(0, curses.COLORS):
		curses.init_pair(i + 1, i, -1)
	for i in range(curses.COLORS):
		try:
			stdscr.addstr(str(i)+"\t",curses.color_pair(i))
		except:
			pass
	try:
		stdscr.getch()
	except: pass
def get_args():
	return [
			"colortest",
			"Displays color palette.",
			None
			]

def run(args):
	curses.wrapper(colortest)