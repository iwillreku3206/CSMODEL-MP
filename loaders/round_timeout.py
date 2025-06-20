from demoparser2 import DemoParser
import pandas as pd

def get_timeout_df(parser: DemoParser):
    vote_cast_df = parser.parse_event('vote_cast')

    rounds_df = parser.parse_ticks(["total_rounds_played"],
                                   ticks=vote_cast_df['tick']).drop_duplicates(
        subset=["tick"]
    ).drop_duplicates(subset="total_rounds_played")

    player_teams = parser.parse_ticks(['team_clan_name'], ticks=[100])[['team_clan_name', 'name']]
    with_user_names_df = pd.merge(vote_cast_df, rounds_df, how='inner', on='tick')

    with_user_names_df.drop(columns='name', inplace=True)
    with_user_names_df.rename(columns={'user_name': 'name'}, inplace=True)
    df = pd.merge(player_teams, with_user_names_df, how='inner', on='name')
    df = df[['team_clan_name', 'total_rounds_played']]
    df.rename(columns={'total_rounds_played': 'round'}, inplace=True)
    return df

def get_timeout_round(df: pd.DataFrame, round: int):
    v = df.loc[df['round'] == round]['team_clan_name'].values
    if len(v) == 0:
        return None
    else:
        return v[0]
