from demoparser2 import DemoParser
from pandas import DataFrame
import pandas as pd

def get_player_spent(parser: DemoParser, name: str, round: int):
    df = parser.parse_ticks(["cash_spent_this_round", "total_rounds_played"]).rename(columns={"user_name": "name"}).drop_duplicates(subset=['name', 'total_rounds_played','cash_spent_this_round'])
    return df.loc[(df['name'] == name) & (df['total_rounds_played'] == round)]['cash_spent_this_round'].values[0]


  


