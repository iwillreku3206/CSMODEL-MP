from demoparser2 import DemoParser
from pandas import DataFrame
import pandas as pd

def get_player_damage_total_df(parser: DemoParser):
    damage_total_df = parser.parse_ticks(['damage_total'])
    damage_total_df['tick'] = damage_total_df['tick'] - 384
    return damage_total_df.drop(columns=['steamid'])
    # Adjust tick to get the true end of round + another 1 second buffer

def get_total_rounds_played_df(parser: DemoParser):
    return parser.parse_ticks(['total_rounds_played'])

def get_player_damage(damage_total_df: DataFrame, total_rounds_played_df: DataFrame, player_name: str, round: int):
    merged_df = pd.merge(damage_total_df, total_rounds_played_df, how='inner', on=['tick', 'name']).drop_duplicates(subset=['total_rounds_played', 'damage_total', 'name'])
    return merged_df.loc[(merged_df['name'] == player_name) & (merged_df['total_rounds_played'] == round)][['damage_total']].values[0][0] - merged_df.loc[(merged_df['name'] == player_name) & (merged_df['total_rounds_played'] == round-1)][['damage_total']].values[0][0]

