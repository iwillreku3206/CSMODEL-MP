import pandas as pd
from demoparser2 import DemoParser
def get_bomb_plant_df(parser: DemoParser):
    df = parser.parse_event("bomb_planted").rename(columns={"user_name": "name"})
    tick_df = parser.parse_ticks(['total_rounds_played', 'last_place_name', 'game_time'], ticks=df['tick'])

    return pd.merge(df, tick_df, how='inner', on=['name', 'tick'])[['total_rounds_played', 'last_place_name', "name", "game_time"]]

def get_bomb_plant_time(df: pd.DataFrame, round: int, round_times: pd.DataFrame):
    v = df.loc[df['total_rounds_played'] == round]['game_time'].values

    if len(v) == 0:
        return None
    else:
        return v[0] - round_times[round]

def get_bomb_planter(df: pd.DataFrame, round: int):
    v = df.loc[df['total_rounds_played'] == round]['name'].values

    if len(v) == 0:
        return None
    else:
        return v[0]

def get_bomb_plant_site(df: pd.DataFrame, round: int):
    v = df.loc[df['total_rounds_played'] == round]['last_place_name'].values

    if len(v) == 0:
        return None
    else:
        return v[0][-1]
