from demoparser2 import DemoParser
from pandas import DataFrame
import pandas as pd

def get_player_spent_amount_df(parser: DemoParser):
    return parser.parse_ticks(["cash_spent_this_round", "total_rounds_played"]).rename(columns={"user_name": "name"}).drop_duplicates(subset=['name', 'total_rounds_played','cash_spent_this_round'])

def get_player_spent(df: DataFrame, name: str, round: int):
    return df.loc[(df['name'] == name) & (df['total_rounds_played'] == round)]['cash_spent_this_round'].values[0]


  


