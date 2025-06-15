import pandas as pd
from demoparser2 import DemoParser

def get_round_length_array(parser: DemoParser):
    s1 = parser.parse_ticks(['game_time'],
                            ticks=parser.parse_event('round_freeze_end')['tick']
                            ).drop_duplicates(subset=['tick'])['game_time']

    df2 = parser.parse_ticks(['game_time'], ticks=parser.parse_event('round_end')['tick']).drop_duplicates(
        subset='tick')

    # we have to drop the first round_end if it happens on tick 1: likely comes from how the match is started by the tournament organizer
    if df2.iloc[0]['tick'] == 1:
        df2.drop([0], inplace=True)

    # magic
    s1 = pd.Series(data=s1.values)
    s2 = pd.Series(data=df2['game_time'].values)

    return (s2 - s1).values
