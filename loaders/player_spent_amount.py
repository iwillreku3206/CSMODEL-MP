from demoparser2 import DemoParser
from pandas import DataFrame
import pandas as pd

def get_player_spent_amount_df(parser: DemoParser):
    return parser.parse_ticks(["cash_spent_this_round"])

def get_total_rounds_played_df(parser: DemoParser):
    return parser.parse_ticks(['total_rounds_played']).drop_duplicates(subset=['total_rounds_played', 'name']).drop(columns=['steamid'])


def get_player_spent(df: DataFrame, df2:DataFrame, name: str, round: int):
    merged_df = pd.merge(df, df2, how='inner', on=['name', 'tick']).drop_duplicates(subset=['name', 'total_rounds_played'])
    return merged_df.loc[(merged_df['name'] == name) & (merged_df['total_rounds_played'] == round)]['cash_spent_this_round'].values[0]

