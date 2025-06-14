from demoparser2 import DemoParser
from pandas import DataFrame
import pandas as pd


def get_player_death(parser: DemoParser, player_name: str, round: int):
    df = parser.parse_event("player_death").rename(columns={"user_name": "name"})
    tick_df = parser.parse_ticks(['total_rounds_played'], ticks=df['tick'])
    df_merged = pd.merge(df, tick_df, how='inner', on=['name', 'tick'])[['total_rounds_played', 'name']]
    return not df_merged.loc[(df_merged['name'] == player_name) & (df_merged['total_rounds_played'] == round)].empty

