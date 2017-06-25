#!/usr/bin/env python3
import argparse
import curses
import importlib

COMMANDS = sorted([
			"matrix",
			"pipes",
			"bounce",
			"colortest",
			"clock",
			"imgbounce",
			"snake",
			"stars"
			])

def main():
	par = argparse.ArgumentParser(prog='tscrnsvr')
	mainsubpar = par.add_subparsers()

	subparsers = {}

	for cmd in COMMANDS:
		module = importlib.import_module("tscrnsvr."+cmd)
		args = module.get_args()
		subparsers[cmd] = mainsubpar.add_parser(args[0],help=args[1])
		if args[2] != None:
			args[2] = sorted(args[2],key=lambda x: x[0][0].lower())
			for argn in args[2]:
				subparsers[cmd].add_argument(*argn[0],**argn[1])
		subparsers[cmd].set_defaults(function=module.run)

	ags = par.parse_args()
	if hasattr(ags,"function"):
		ags.function(ags)
	else:
		par.print_help()