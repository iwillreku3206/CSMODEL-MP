from demoparser2 import DemoParser
from pandas import DataFrame
import pandas as pd

def get_round_first_kill(df: DataFrame, tick_df:DataFrame, name: str, round: int):
    merged_df = pd.merge(df, tick_df, how='inner', on=['tick'])[['attacker_name', 'total_rounds_played']]
    merged_df = merged_df.drop_duplicates(subset=['total_rounds_played'])
    return not merged_df.loc[(merged_df['total_rounds_played'] == round - 1) & (merged_df['attacker_name'] == name)]['attacker_name'].empty

