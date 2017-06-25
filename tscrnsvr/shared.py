import curses
import base64
import math
import time

class ScreenSpace:
	def __init__(self,win):
		self.win	= win
		self.size	= self.win.getmaxyx()
		curses.start_color()
		curses.use_default_colors()
		self.win.nodelay(1)
		for i in range(0, curses.COLORS):
			curses.init_pair(i + 1, i, -1)
		curses.curs_set(0)
	def addchar(self,x,y,char,mods):
		self.size = self.win.getmaxyx()
		#print(x,y,char,mods)
		try:
			self.win.addstr(int(y),int(x),chr(char),curses.color_pair(mods))
		except:
			pass
	def addstr(self,x,y,str,mods):
		self.size = self.win.getmaxyx()
		try:
			self.win.addstr(int(y),int(x),str,curses.color_pair(mods))
		except:
			pass
	def render(self,debug=None,clear=True,ref=True):
		self.size = self.win.getmaxyx()
		if debug != None:
			for dstr in range(len(debug)):
				self.win.addstr(dstr,0,debug[dstr],curses.color_pair(0))
		if ref == True:
			self.win.refresh()
		if clear == True:
			self.win.erase()
	def destroy(self):
		curses.nocbreak()
		self.win.keypad(0)
		curses.echo()
		curses.endwin()
		curses.curs_set(1)
	def in_bounds(self, x, y):
		self.size = self.win.getmaxyx()
		if y >= 0:
			if y < self.size[0]:
				if x >= 0:
					if x < self.size[1]:
						return True
		return False

class ColorObj:
	def __init__(self):
		self.colorstr = [ 	
			"AAAAwoAAAADCgADCgMKAAAAAwoDCgADCgADCgMKAw4DDgMOAwoDCgMKAw78A",
			"AADDvwDDv8O/AAAAw7/DvwDDvwDDv8O/w78Aw7/Dv8O/w78AAAAAAF8AAMKH",
			"AADCrwAAw5cAAMO/AF8AAF9fAF/ChwBfwq8AX8OXAF/DvwDChwAAwodfAMKH",
			"wocAwofCrwDCh8OXAMKHw78Awq8AAMKvXwDCr8KHAMKvwq8Awq/DlwDCr8O/",
			"AMOXAADDl18Aw5fChwDDl8KvAMOXw5cAw5fDvwDDvwAAw79fAMO/wocAw7/C",
			"rwDDv8OXAMO/w79fAABfAF9fAMKHXwDCr18Aw5dfAMO/X18AX19fX1/Ch19f",
			"wq9fX8OXX1/Dv1/ChwBfwodfX8KHwodfwofCr1/Ch8OXX8KHw79fwq8AX8Kv",
			"X1/Cr8KHX8Kvwq9fwq/Dl1/Cr8O/X8OXAF/Dl19fw5fCh1/Dl8KvX8OXw5df",
			"w5fDv1/DvwBfw79fX8O/wodfw7/Cr1/Dv8OXX8O/w7/ChwAAwocAX8KHAMKH",
			"wocAwq/ChwDDl8KHAMO/wodfAMKHX1/Ch1/Ch8KHX8Kvwodfw5fCh1/Dv8KH",
			"wocAwofCh1/Ch8KHwofCh8KHwq/Ch8KHw5fCh8KHw7/Ch8KvAMKHwq9fwofC",
			"r8KHwofCr8KvwofCr8OXwofCr8O/wofDlwDCh8OXX8KHw5fCh8KHw5fCr8KH",
			"w5fDl8KHw5fDv8KHw78AwofDv1/Ch8O/wofCh8O/wq/Ch8O/w5fCh8O/w7/C",
			"rwAAwq8AX8KvAMKHwq8Awq/CrwDDl8KvAMO/wq9fAMKvX1/Cr1/Ch8KvX8Kv",
			"wq9fw5fCr1/Dv8KvwocAwq/Ch1/Cr8KHwofCr8KHwq/Cr8KHw5fCr8KHw7/C",
			"r8KvAMKvwq9fwq/Cr8KHwq/Cr8Kvwq/Cr8OXwq/Cr8O/wq/DlwDCr8OXX8Kv",
			"w5fCh8Kvw5fCr8Kvw5fDl8Kvw5fDv8Kvw78Awq/Dv1/Cr8O/wofCr8O/wq/C",
			"r8O/w5fCr8O/w7/DlwAAw5cAX8OXAMKHw5cAwq/DlwDDl8OXAMO/w5dfAMOX",
			"X1/Dl1/Ch8OXX8Kvw5dfw5fDl1/Dv8OXwocAw5fCh1/Dl8KHwofDl8KHwq/D",
			"l8KHw5fDl8KHw7/Dl8KvAMOXwq9fw5fCr8KHw5fCr8Kvw5fCr8OXw5fCr8O/",
			"w5fDlwDDl8OXX8OXw5fCh8OXw5fCr8OXw5fDl8OXw5fDv8OXw78Aw5fDv1/D",
			"l8O/wofDl8O/wq/Dl8O/w5fDl8O/w7/DvwAAw78AX8O/AMKHw78Awq/DvwDD",
			"l8O/AMO/w79fAMO/X1/Dv1/Ch8O/X8Kvw79fw5fDv1/Dv8O/wocAw7/Ch1/D",
			"v8KHwofDv8KHwq/Dv8KHw5fDv8KHw7/Dv8KvAMO/wq9fw7/Cr8KHw7/Cr8Kv",
			"w7/Cr8OXw7/Cr8O/w7/DlwDDv8OXX8O/w5fCh8O/w5fCr8O/w5fDl8O/w5fD",
			"v8O/w78Aw7/Dv1/Dv8O/wofDv8O/wq/Dv8O/w5fDv8O/w78ICAgSEhIcHBwm",
			"JiYwMDA6OjpEREROTk5YWFhgYGBmZmZ2dnbCgMKAwoDCisKKworClMKUwpTC",
			"nsKewp7CqMKowqjCssKywrLCvMK8wrzDhsOGw4bDkMOQw5DDmsOaw5rDpMOk",
			"w6TDrsOuw64=" ]
		self.rcolors = [ord(c) for c in base64.b64decode(''.join(self.colorstr)).decode("utf-8")]
		self.colors = {}
		self.cn = 0
		for a, b, c in zip(*[iter(self.rcolors)]*3): self.colors[self.cn] = ((a,b,c)); self.cn += 1
		self.rcolors = {v: k for k, v in self.colors.items()}

	def colorDistance(self, c1, c2):
		try:
			(r1,g1,b1) = c1
			(r2,g2,b2) = c2
			return math.sqrt((r1 - r2)**2 + (g1 - g2) ** 2 + (b1 - b2) **2)
		except:
			return -1

	def approxColor(self,cl):
		closest_colors = sorted(self.rcolors, key=lambda color: self.colorDistance(color, cl))
		return self.rcolors[closest_colors[0]]

def print_error(s):
	print("\x1b[31m%s\x1b[0m" % s)

def get_center(win):
	dims = win.getmaxyx()
	return [round(dims[1]/2),round(dims[0]/2)]
	
def parse_chars(chrl):
	charlist = []
	try:
		chrl = chrl.split(",")
		for chrr in chrl:
			if "-" in chrr:
				dashs = chrr.split("-")
				if len(dashs) == 2:
					charlist.extend(range(int(dashs[0]),int(dashs[1])))
			elif chrr != "":
				charlist.append(int(chrr))
			assert len(charlist) > 0
		return charlist
	except:
		print_error("MATRIX ERROR: Could not parse characters list!")
		sys.exit(1)
	