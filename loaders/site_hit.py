from demoparser2 import DemoParser
from pandas import DataFrame
def get_site_hit_df(parser):
    df = parser.parse_ticks(['team_name', 'last_place_name', 'total_rounds_played', 'game_time'])
    # name, steamid, tick, team_name
    return df.loc[
        (df['team_name'] == 'TERRORIST')
        & ((df['last_place_name'] == 'BombsiteA') | (df['last_place_name'] == 'BombsiteB'))
    ].drop(columns=['name', 'steamid', 'tick', 'team_name']).drop_duplicates(subset=['total_rounds_played', 'last_place_name'])

def get_site_hit_time(site_hit_df: DataFrame, round_times: list[int], round: int):
    values = site_hit_df.loc[site_hit_df['total_rounds_played'] == round - 1]['game_time'].values
    if len(values) == 0:
        return None
    else:
        return values[0] - round_times[round - 1]

def get_site_hit(site_hit_df: DataFrame, round: int):
    values = site_hit_df.loc[site_hit_df['total_rounds_played'] == round - 1]['last_place_name'].values
    if len(values) == 0:
        return None
    else:
        return values[0][-1]
