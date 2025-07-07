
from demoparser2 import DemoParser
import pandas as pd
import os
import sys

from loaders.mapname import get_mapname


def parse_demo(filename: str):
# parse filename
# file names are a tuple of matchid_mapid.dem
    parser = DemoParser(filename)
    filename_info = filename.split(os.sep)[-1][:-4].split('_')
    matchid = int(filename_info[0])
    mapid = int(filename_info[1])

    map_player_rounds = []
    round_count = parser.parse_event("round_freeze_end").shape[0]
    parser = DemoParser(filename)

    players = parser.parse_player_info()
    mapname = get_mapname(parser)
    player_teams = parser.parse_ticks(['team_clan_name'], ticks=[100])[['team_clan_name', 'name']]

    df = parser.parse_event('smokegrenade_detonate')
    ticks_df = parser.parse_ticks(['total_rounds_played'])
    ticks_df.rename(columns={'name': 'user_name'}, inplace=True)
    ticks_df['tick'] = ticks_df['tick'] + 640
    df = pd.merge(df, ticks_df, how='inner', on=['tick', 'user_name']).drop_duplicates(subset=['total_rounds_played', 'tick', 'user_name'])
    df['map_name'] = mapname
    df['matchid'] = matchid
    df['mapid'] = mapid
    df['player_team'] = df['user_name'].map(player_teams.set_index('name')['team_clan_name'])
    df.rename(columns={'total_rounds_played': 'round_number'}, inplace=True)
    df['round_number'] = df['round_number'] + 1

    return df

if len(sys.argv) < 2:
	print('Usage: python read_demo_for_smoke.py <demo_name>.dem')
	exit()

dem = parse_demo(sys.argv[1])
pd.DataFrame(dem).to_csv(sys.argv[1] + "_smoke.csv", index=False)


        