#!/usr/bin/env python3

from demoparser2 import DemoParser
import pandas as pd
import os

from loaders.mapname import get_mapname

# read current directory
# get list of demos
# parse each demo
# each demo outputs a 2d array
# all demos combined will be a large 2d array
# convert large 2d array to csv
# write csv

def parse_demo(filename: str):
	# parse filename
	# file names are a tuple of matchid_mapid_roundidoffset.dem

	filename_info = filename.split(os.sep)[-1][:-4].split('_')
	matchid = int(filename_info[0])
	mapid = int(filename_info[1])
	roundidoffset = int(filename_info[2])

	map_player_rounds = []

	parser = DemoParser(filename)
	round_count = parser.parse_event("round_freeze_end").shape[0]
	players = parser.parse_player_info()
	mapname = get_mapname(parser)
	player_teams = parser.parse_ticks(['team_clan_name'], ticks=[100])[['team_clan_name', 'name']]

	for r in range(round_count):
		for p in range(players.shape[0]):
			player_name = players['name'][p]
			player_team = player_teams.loc[player_teams['name'] == player_name]['team_clan_name'].values[0]
			# parse each player-round here
			map_player_rounds += [[
				matchid,           # match_id
				mapid,             # map_id
				r + roundidoffset, # round_id
				player_team,       # team_name
				mapname,           # map_name
				r + 1,             # round_number
				None,              # round_ct_team
				None,              # round_first_site_hit
				None,              # round_site_hit_time
				None,              # round_bomb_plant_site
				None,              # round_bomb_plant_time
				None,              # round_length
				None,              # round_result
				None,              # round_timeout_called_before
				player_name,       # player_name
				None,              # player_flashes_used
				None,              # player_smokes_used
				None,              # player_grenades_used
				None,              # player_molotovs_used
				None,              # player_incendiaries_used
				None,              # player_kills
				None,              # player_died
				None,              # player_spent_amount
				[],                # player_loadout
				None,              # player_damage
				None,              # round_first_killer
				None,              # round_first_death
				None,              # player_headshots
				None,              # player_torsoshots
				None,              # player_stomachshots
				None,              # player_legshots
				None,              # player_planted_bomb
			]]
			pass

	return map_player_rounds


# if for scripts i forgor how to do
dem = parse_demo('C:\\Users\\rek\\Downloads\\analyzing_cs2_demo\\0_0_0.dem')
print(dem)
