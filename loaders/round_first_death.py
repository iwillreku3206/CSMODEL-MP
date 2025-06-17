from demoparser2 import DemoParser
from pandas import DataFrame
import pandas as pd
import xlwings as xl

def get_round_first_death(parser: DemoParser, round: int):
    df = parser.parse_event("player_death")
    df['tick'] = df['tick'] - 64*6 # tick adjust to get the true end of round + another 1 second buffer
    # since the start of the round is 20 seconds, the first death/kill will not have a negative tick
    tick_df = parser.parse_ticks(['total_rounds_played'], ticks=df['tick'])
    merged_df = pd.merge(df, tick_df, how='inner', on=['tick'])[['user_name', 'total_rounds_played']]
    merged_df = merged_df.drop_duplicates(subset=['total_rounds_played'])
    return merged_df.loc[(merged_df['total_rounds_played'] == round - 1)]['user_name'].values[0]