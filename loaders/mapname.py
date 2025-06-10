from demoparser2 import DemoParser
import pandas as pd

def get_mapname(parser: DemoParser):
	return parser.parse_header()['map_name']
