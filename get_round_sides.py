from demoparser2 import DemoParser
import pandas as pd
import os
import sys

global out_data
out_data = []

def parse(filename: str):
    global out_data
    parser = DemoParser(filename)
    filename_info = filename.split(os.sep)[-1][:-4].split('_')
    matchid = int(filename_info[0])
    mapid = int(filename_info[1])

    df1 = parser.parse_ticks(['team_clan_name', 'team_name'], ticks=parser.parse_event('round_freeze_end')['tick'])
    df2 = parser.parse_player_info().drop_duplicates(subset='team_number')
    df3 = pd.merge(df1, df2, on="name", how="inner")
    vals = df3.query('team_name == "CT"')['team_clan_name'].values
    print(len(vals))
    i = 0
    while i < len(vals):
        print(i)
        out_data += [{"matchid": matchid, "mapid": mapid, "round_number": i + 1, "round_ct_team": vals[i]}]
        i += 1

for filename in os.listdir(sys.argv[1]):
    if filename.endswith(".dem"):
        print("Parsing: " + filename)
        parse(filename)

    df = pd.DataFrame(out_data)
    df.to_csv("ct_teams.csv", index=False)
