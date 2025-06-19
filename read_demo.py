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
from loaders.player_kills import get_player_kill_counts, get_player_kill_count
from loaders.player_shots import player_shots_all, get_player_shots
from loaders.bomb_plants import load_bomb_plants, get_bomb_planted
from loaders.bomb_defuse import get_bomb_defuses, is_bomb_defused
from loaders.round_result import get_round_result_array
from loaders.round_length import get_round_length_array
from loaders.player_damage import get_player_damage_total_df, get_player_damage, get_total_rounds_played_df
from loaders.player_death import get_player_death_df, get_player_death, get_total_rounds_played_with_tickset_df
from loaders.player_spent_amount import get_player_spent_amount_df, get_player_spent
from loaders.round_first_death import get_round_first_death
from loaders.round_first_kill import get_round_first_kill
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
	round_start_times_df = pd.DataFrame(
		{"total_rounds_played": [x for x in range(len(round_start_times))], "round_start_time": round_start_times})
	site_hit_df = get_site_hit_df(parser, round_start_times)
	ct_teams = get_ct_teams(parser)
	bomb_plants = get_bomb_plant_df(parser)
	round_results = get_round_result_array(parser)
	print(round_results)
	round_lengths = get_round_length_array(parser)

	player_kills_df = get_player_kill_counts(parser)
	player_headshots_df = player_shots_all(parser, 'head')
	player_upperbodyshots_df = player_shots_all(parser, 'upperbody')
	player_stomachshots_df = player_shots_all(parser, 'stomach')
	player_legshots_df = player_shots_all(parser, 'legs')

	bomb_plants_df = load_bomb_plants(parser)
	get_bomb_defuses_df = get_bomb_defuses(parser)
	
	player_damage_total_df = get_player_damage_total_df(parser)
	total_rounds_played_df= get_total_rounds_played_df(parser)

	player_death_df = get_player_death_df(parser)
	total_rounds_played_df_player_death = get_total_rounds_played_with_tickset_df(parser, player_death_df)

	player_spent_amount_df = get_player_spent_amount_df(parser)
	
	

	for r in range(round_count):
		print("parsed " + str(r) + " rounds")
		round_ct_team = get_ct_team_for_round(ct_teams, r)
		for p in range(players.shape[0]):
			player_name = players['name'][p]
			player_team = player_teams.loc[player_teams['name'] == player_name]['team_clan_name'].values[0]
			# parse each player-round here
			map_player_rounds += [[
				matchid,                            										#00 match_id
				mapid,                              										#01 map_id
				0,                  										                #02 round_id - to be fixed
				player_team,                        										#03 team_name
				mapname,                            										#04 map_name
				r + 1,                              										#05 round_number
				round_ct_team,                      										#06 round_ct_team
				get_site_hit(site_hit_df, r),   							    			#07 round_first_site_hit
				get_site_hit_time(site_hit_df, round_start_times, r),   #08 round_site_hit_time
				get_bomb_plant_site(bomb_plants, r),                    #09 round_bomb_plant_site
				get_bomb_plant_time(bomb_plants, r, round_start_times), #10 round_bomb_plant_time
				get_bomb_planted(bomb_plants_df, r, player_name),       #11 round_bomb_planter
				None,                                                   #12 round_defuse_time
				is_bomb_defused(get_bomb_defuses_df, r, player_name), 	#13 round_bomb_is_defuser
				round_lengths[r],                               		#14 round_length
				round_results[r],                               		#15 round_result
				None,                               					#16 round_timeout_called_before
				player_name,                        					#17 player_name
				None,                               					#18 player_flashes_used
				None,                               					#19 player_smokes_used
				None,                               					#20 player_grenades_used
				None,                               					#21 player_molotovs_used
				None,                               					#22 player_incendiaries_used
				get_player_kill_count(player_kills_df, r, player_name), #23 player_kills
				get_player_death(player_death_df, total_rounds_played_df_player_death, player_name, r),         #24 player_died                            										#22 player_died
				get_player_spent(player_spent_amount_df, player_name, r), 										#25 player_spent_amount
				[],                                 							                                #26 player_loadout
				get_player_damage(player_damage_total_df, total_rounds_played_df, player_name, r+1),            #27 player_damage                   										#25 player_damage
				get_round_first_kill(player_death_df, total_rounds_played_df_player_death, player_name, r+1),   #28 round_first_killer                            										#26 round_first_killer
				get_round_first_death(player_death_df, total_rounds_played_df_player_death, player_name, r+1),  #29 round_first_death                             										#27 round_first_death
				get_player_shots(player_headshots_df, 'head', r, player_name), 				#30 player_headshots
				get_player_shots(player_upperbodyshots_df, 'upperbody', r, player_name), 	#31 player_upperbodyshots
				get_player_shots(player_stomachshots_df, 'stomach', r, player_name), 		#32 player_stomachshots
				get_player_shots(player_legshots_df, 'legs', r, player_name), 				#33 player_legshots
			]]

	return map_player_rounds


# if for scripts i forgor how to do

dem = parse_demo('C:\\Users\\rek\\Downloads\\analyzing_cs2_demo\\28_68.dem')
pd.DataFrame(dem).to_csv("test.csv")
