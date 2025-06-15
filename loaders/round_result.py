from demoparser2 import DemoParser
import pandas as pd

def get_round_result_array(parser: DemoParser):
    df = parser.parse_event('round_end')

    # i love round_end having tick 1 being an end round thanks esl
    if df.iloc[0]['tick'] == 1:
        df.drop(index=0, inplace=True)

    return pd.merge(parser.parse_ticks(['total_rounds_played'], ticks=df['tick']).drop_duplicates(subset=["tick"]), df,
             how='inner', on=['tick'])['winner'].values