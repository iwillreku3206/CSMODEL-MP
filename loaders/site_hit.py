from demoparser2 import DemoParser
from pandas import DataFrame
import pandas as pd
def get_site_hit_df(parser, round_times: list[int]):
    df = parser.parse_ticks(['team_name', 'last_place_name', 'total_rounds_played', 'game_time'])
    # name, steamid, tick, team_name
    df = df.loc[
        (df['team_name'] == 'TERRORIST')
        & ((df['last_place_name'] == 'BombsiteA') | (df['last_place_name'] == 'BombsiteB'))
    ].drop(columns=['name', 'steamid', 'team_name']).drop_duplicates(subset=['total_rounds_played', 'last_place_name'])
    rounds_df = pd.DataFrame({"total_rounds_played": [x for x in range(len(round_times))], "round_start_time": round_times})
    df = pd.merge(df, rounds_df, how="inner", on=["total_rounds_played"])
    df = df.loc[df['game_time'] > df['round_start_time']]
    return df

def get_site_hit_time(site_hit_df: DataFrame, round_times: list[int], round: int):
    values = site_hit_df.loc[site_hit_df['total_rounds_played'] == round]['game_time'].values
    if len(values) == 0:
        return None
    else:
        return values[0] - round_times[round]

def get_site_hit(site_hit_df: DataFrame, round: int):
    values = site_hit_df.loc[site_hit_df['total_rounds_played'] == round]['last_place_name'].values
    if len(values) == 0:
        return None
    else:
        return values[0][-1]
