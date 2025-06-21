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
from loaders.bomb_defuse import get_bomb_defuses, is_bomb_defused, bomb_defuse_time
from loaders.round_result import get_round_result_array
from loaders.round_length import get_round_length_array
from loaders.player_damage import get_player_damage_total_df, get_player_damage, get_total_rounds_played_df
from loaders.player_death import get_player_death_df, get_player_death, get_total_rounds_played_with_tickset_df
from loaders.player_spent_amount import get_player_spent_amount_df, get_player_spent
from loaders.round_first_death import get_round_first_death
from loaders.round_first_kill import get_round_first_kill
from loaders.player_utilities import get_utils_thrown, count_utils_thrown
from loaders.player_loadout import get_all_loadouts_at_round_freeze_end, get_player_loadout_at_round_freeze_end
from loaders.helper import get_round_start_ticks, get_round_freeze_end_ticks
from loaders.round_timeout import get_timeout_df, get_timeout_round

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
	get_bomb_defuses_df = get_bomb_defuses(parser, round_start_times_df)

	player_damage_total_df = get_player_damage_total_df(parser)
	total_rounds_played_df= get_total_rounds_played_df(parser)

	player_death_df = get_player_death_df(parser)
	total_rounds_played_df_player_death = get_total_rounds_played_with_tickset_df(parser, player_death_df)

	player_spent_amount_df = get_player_spent_amount_df(parser)

	round_start_ticks = get_round_start_ticks(parser)
	round_freeze_end_ticks = get_round_freeze_end_ticks(parser)
	utils_thrown = get_utils_thrown(parser)
	loadouts = get_all_loadouts_at_round_freeze_end(parser, round_freeze_end_ticks)

	timeout_df = get_timeout_df(parser)

	for r in range(round_count):
		print("parsed " + str(r) + " rounds")
		round_ct_team = get_ct_team_for_round(ct_teams, r)
		for p in range(players.shape[0]):
			player_name = players['name'][p]
			player_team = player_teams.loc[player_teams['name'] == player_name]['team_clan_name'].values[0]

			# Get the tick of round start and end (mostly used in functions made by @EvilConundrum)
			round_start_tick = round_start_ticks[r]
			round_end_tick = round_start_ticks[r + 1]
			round_freeze_end_tick = round_freeze_end_ticks[r]

			# parse each player-round here
			map_player_rounds += [{
				'match_id':						matchid,                            					#00 match_id
				'map_id':						mapid,                              					#01 map_id
				'round_id':						0,                  									#02 round_id - to be fixed
				'team_name':					player_team,                        					#03 team_name
				'map_name':						mapname,                            					#04 map_name
				'round_number':					r + 1,                              					#05 round_number
				'round_ct_team':				round_ct_team,                      					#06 round_ct_team
				'round_first_site_hit':			get_site_hit(site_hit_df, r),   						#07 round_first_site_hit
				'round_site_hit_time':			get_site_hit_time(site_hit_df, round_start_times, r),   #08 round_site_hit_time
				'round_bomb_plant_site':		get_bomb_plant_site(bomb_plants, r),                    #09 round_bomb_plant_site
				'player_planted_bomb':			get_bomb_planted(bomb_plants_df, r, player_name),       #32 player_planted_bomb
				'round_bomb_plant_time':		get_bomb_plant_time(bomb_plants, r, round_start_times), #10 round_bomb_plant_time
				'round_bomb_defuser':			is_bomb_defused(get_bomb_defuses_df, r, player_name), 	#11 round_bomb_defuser
				'bomb_defuse_time':				bomb_defuse_time(get_bomb_defuses_df, r),               #XX bomb_defuse_time
				'round_length':					round_lengths[r],                               		#12 round_length
				'round_result':					round_results[r],                               		#13 round_result
				'round_timeout_called_before':	get_timeout_round(timeout_df, r),      					#14 round_timeout_called_before
				'player_name':					player_name,                        					#15 player_name
				'player_flashes_used':			count_utils_thrown(utils_thrown, player_name, round_start_tick, round_end_tick, 'weapon_flashbang'),                               										#16 player_flashes_used
				'player_smokes_used':			count_utils_thrown(utils_thrown, player_name, round_start_tick, round_end_tick, 'weapon_smokegrenade'),                               										#17 player_smokes_used
				'player_grenades_used':			count_utils_thrown(utils_thrown, player_name, round_start_tick, round_end_tick, 'weapon_hegrenade'),                               										#18 player_grenades_used
				'player_molotovs_used':			count_utils_thrown(utils_thrown, player_name, round_start_tick, round_end_tick, 'weapon_molotov'),                               										#19 player_molotovs_used
				'player_incendiaries_used':		count_utils_thrown(utils_thrown, player_name, round_start_tick, round_end_tick, 'weapon_incgrenade'),                               										#20 player_incendiaries_used
				'player_kills':					get_player_kill_count(player_kills_df, r, player_name), #21 player_kills
				'player_died':					get_player_death(player_death_df, total_rounds_played_df_player_death, player_name, r),                               										#22 player_died
				'player_spent_amount':			get_player_spent(player_spent_amount_df, total_rounds_played_df, player_name, r+1),                               										#23 player_spent_amount
				'player_loadout':				get_player_loadout_at_round_freeze_end(loadouts, player_name, round_freeze_end_tick),                                 										#24 player_loadout
				'player_damage':				get_player_damage(player_damage_total_df, total_rounds_played_df, player_name, r+1),                               										#25 player_damage
				'round_first_killer':			get_round_first_kill(player_death_df, total_rounds_played_df_player_death, player_name, r+1),                               										#26 round_first_killer
				'round_first_death':			get_round_first_death(player_death_df, total_rounds_played_df_player_death, player_name, r+1),                               										#27 round_first_death
				'player_headshots':				get_player_shots(player_headshots_df, 'head', r, player_name), 				#28 player_headshots
				'player_upperbodyshots':		get_player_shots(player_upperbodyshots_df, 'upperbody', r, player_name), 	#29 player_upperbodyshots
				'player_stomachshots':			get_player_shots(player_stomachshots_df, 'stomach', r, player_name), 		#30 player_stomachshots
				'player_legshots':				get_player_shots(player_legshots_df, 'legs', r, player_name), 				#31 player_legshots
			}]

	return map_player_rounds


# if for scripts i forgor how to do

dem = parse_demo('C:\\Users\\rek\\Downloads\\analyzing_cs2_demo\\28_68.dem')
pd.DataFrame(dem).to_csv("test.csv", index=False)
