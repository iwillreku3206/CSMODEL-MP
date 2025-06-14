#!/usr/bin/env python3

from demoparser2 import DemoParser
import pandas as pd
import os

from loaders.bomb_plant import get_bomb_plant_df, get_bomb_plant_site, get_bomb_planter, get_bomb_plant_time
from loaders.game_time_offset import get_game_time_offset
from loaders.mapname import get_mapname
from loaders.ct_team import get_ct_team_for_round, get_ct_teams
from loaders.game_time_offset import get_game_time_offset
from loaders.round_time import get_round_start_times
from loaders.site_hit import get_site_hit_df, get_site_hit, get_site_hit_time

# read current directory
# get list of demos
# parse each demo
# each demo outputs a 2d array
# all demos combined will be a large 2d array
# convert large 2d array to csv
# write csv

def parse_demo(filename: str):
	# parse filename
	# file names are a tuple of matchid_mapid.dem

	filename_info = filename.split(os.sep)[-1][:-4].split('_')
	matchid = int(filename_info[0])
	mapid = int(filename_info[1])

	map_player_rounds = []

	parser = DemoParser(filename)
	round_count = parser.parse_event("round_freeze_end").shape[0]
	players = parser.parse_player_info()
	mapname = get_mapname(parser)
	player_teams = parser.parse_ticks(['team_clan_name'], ticks=[100])[['team_clan_name', 'name']]
	game_time_offset = get_game_time_offset(parser)
	round_start_times = get_round_start_times(parser)
	site_hit_df = get_site_hit_df(parser)
	ct_teams = get_ct_teams(parser)
	bomb_plants = get_bomb_plant_df(parser)

	for r in range(round_count):
		round_ct_team = get_ct_team_for_round(ct_teams, r)
		for p in range(players.shape[0]):
			player_name = players['name'][p]
			player_team = player_teams.loc[player_teams['name'] == player_name]['team_clan_name'].values[0]
			# parse each player-round here
			map_player_rounds += [[
				matchid,                            # match_id
				mapid,                              # map_id
				0,                                  # round_id; to be fixed when we combine the data
				player_team,                        # team_name
				mapname,                            # map_name
				r + 1,                              # round_number
				round_ct_team,                      # round_ct_team
				get_site_hit(site_hit_df, r + 1),                                # round_first_site_hit
				get_site_hit_time(site_hit_df, round_start_times, r + 1),        # round_site_hit_time
				get_bomb_plant_site(bomb_plants, r),                             # round_bomb_plant_site
				get_bomb_planter(bomb_plants, r),                                # round_bomb_planter
				get_bomb_plant_time(bomb_plants, r, round_start_times),          # round_bomb_plant_time
				None,                               # round_length
				None,                               # round_result
				None,                               # round_timeout_called_before
				player_name,                        # player_name
				None,                               # player_flashes_used
				None,                               # player_smokes_used
				None,                               # player_grenades_used
				None,                               # player_molotovs_used
				None,                               # player_incendiaries_used
				None,                               # player_kills
				None,                               # player_died
				None,                               # player_spent_amount
				[],                                 # player_loadout
				None,                               # player_damage
				None,                               # round_first_killer
				None,                               # round_first_death
				None,                               # player_headshots
				None,                               # player_torsoshots
				None,                               # player_stomachshots
				None,                               # player_legshots
				None,                               # player_planted_bomb
			]]
			pass

	return map_player_rounds


# if for scripts i forgor how to do
dem = parse_demo('C:\\Users\\rek\\Downloads\\analyzing_cs2_demo\\14_33.dem')
print(dem)
