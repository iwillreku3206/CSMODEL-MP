#!/usr/bin/env python3

from demoparser2 import DemoParser
import pandas as pd

from loaders.mapname import get_mapname

# read current directory
# get list of demos
# parse each demo
# each demo outputs a 2d array
# all demos combined will be a large 2d array
# convert large 2d array to csv
# write csv

def parse_demo(filename):
	parser = DemoParser(filename)
	return [
		get_mapname(parser)
	]


# if for scripts i forgor how to do
print(parse_demo('C:\\Users\\rek\\Downloads\\analyzing_cs2_demo\\falcons-vs-vitality-m5-nuke.dem'))
