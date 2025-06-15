from demoparser2 import DemoParser
from pandas import DataFrame
import pandas as pd

def get_player_hurt_df(parser: DemoParser, player_name: str, round: int):
    df = parser.parse_ticks(["damage_total"])
    df['tick'] = df['tick'] - 320
    tick_df = parser.parse_ticks(['total_rounds_played'])
    merged_df = pd.merge(df, tick_df, how='inner', on=['tick', 'name']).drop_duplicates(subset=['total_rounds_played', 'damage_total', 'name'])
    return merged_df.loc[(merged_df['name'] == player_name) & (merged_df['total_rounds_played'] == round)][['damage_total']].values[0][0] - merged_df.loc[(merged_df['name'] == player_name) & (merged_df['total_rounds_played'] == round-1)][['damage_total']].values[0][0]

