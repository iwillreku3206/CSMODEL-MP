from demoparser2 import DemoParser
from pandas import DataFrame
import pandas as pd

def get_total_rounds_played_with_tickset_df(parser: DemoParser, df: DataFrame):
    return parser.parse_ticks(['total_rounds_played'], ticks=df['tick'])

def get_player_death_df(parser: DemoParser):
    df = parser.parse_event("player_death").rename(columns={"user_name": "name"})
    df['tick'] = df['tick'] - 64 * 10  # Adjust tick to get the true end of round + another 1 second buffer
    return df 

def get_player_death(player_death_df: DataFrame, total_rounds_played_df: DataFrame, player_name: str, round: int):
    df_merged = pd.merge(player_death_df, total_rounds_played_df, how='inner', on=['name', 'tick'])[['total_rounds_played', 'name']]
    return not df_merged.loc[(df_merged['name'] == player_name) & (df_merged['total_rounds_played'] == round)].empty

