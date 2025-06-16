#!/usr/bin/env python3

from demoparser2 import DemoParser
import pandas as pd
import os

from loaders.game_time_offset import get_game_time_offset
from loaders.mapname import get_mapname
from loaders.ct_team import get_ct_team_for_round, get_ct_teams
from loaders.game_time_offset import get_game_time_offset
from loaders.round_time import get_round_start_times
from loaders.site_hit import get_site_hit_df, get_site_hit, get_site_hit_time
from loaders.player_kills import get_player_kill_counts, get_player_kill_count
from loaders.player_shots import player_shots_all, get_player_shots
from loaders.bomb_plants import load_bomb_plants, get_bomb_planted
from loaders.bomb_defuse import get_bomb_defuses, is_bomb_defused

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
	game_time_offset = get_game_time_offset(parser)
	round_start_times = get_round_start_times(parser)
	site_hit_df = get_site_hit_df(parser)
	ct_teams = get_ct_teams(parser)

	player_kills_df = get_player_kill_counts(parser)
	player_headshots_df = player_shots_all(parser, 'head')
	player_upperbodyshots_df = player_shots_all(parser, 'upperbody')
	player_stomachshots_df = player_shots_all(parser, 'stomach')
	player_legshots_df = player_shots_all(parser, 'legs')

	bomb_plants_df = load_bomb_plants(parser)
	get_bomb_defuses_df = get_bomb_defuses(parser)
	

	for r in range(round_count):
		round_ct_team = get_ct_team_for_round(ct_teams, r)
		for p in range(players.shape[0]):
			player_name = players['name'][p]
			player_team = player_teams.loc[player_teams['name'] == player_name]['team_clan_name'].values[0]
			# parse each player-round here
			map_player_rounds += [[
				matchid,                            										#00 match_id
				mapid,                              										#01 map_id
				r + roundidoffset,                  										#02 round_id
				player_team,                        										#03 team_name
				mapname,                            										#04 map_name
				r + 1,                              										#05 round_number
				round_ct_team,                      										#06 round_ct_team
				get_site_hit(site_hit_df, r + 1),   										#07 round_first_site_hit
				get_site_hit_time(site_hit_df, round_start_times, r + 1),   				#08 round_site_hit_time
				None,                               										#09 round_bomb_plant_site
				None,                               										#10 round_bomb_plant_time
				is_bomb_defused(get_bomb_defuses_df, r, player_name), 						#11 round_bomb_defuser
				None,                               										#12 round_length
				None,                               										#13 round_result
				None,                               										#14 round_timeout_called_before
				player_name,                        										#15 player_name
				None,                               										#16 player_flashes_used
				None,                               										#17 player_smokes_used
				None,                               										#18 player_grenades_used
				None,                               										#19 player_molotovs_used
				None,                               										#20 player_incendiaries_used
				get_player_kill_count(player_kills_df, r, player_name),						#21 player_kills
				None,                               										#22 player_died
				None,                               										#23 player_spent_amount
				[],                                 										#24 player_loadout
				None,                               										#25 player_damage
				None,                               										#26 round_first_killer
				None,                               										#27 round_first_death
				get_player_shots(player_headshots_df, 'head', r, player_name), 				#28 player_headshots
				get_player_shots(player_upperbodyshots_df, 'upperbody', r, player_name), 	#29 player_upperbodyshots
				get_player_shots(player_stomachshots_df, 'stomach', r, player_name), 		#30 player_stomachshots
				get_player_shots(player_legshots_df, 'legs', r, player_name), 				#31 player_legshots
				get_bomb_planted(bomb_plants_df, r, player_name),                           #32 player_planted_bomb
			]]

	return map_player_rounds


# if for scripts i forgor how to do
dem = pd.DataFrame(parse_demo('demos\\0_0_0.dem'))
dem.to_csv('csvdump\\0_0_0.csv', index=False)
