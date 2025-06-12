from demoparser2 import DemoParser

def get_ct_teams(parser: DemoParser):
    df = parser.parse_ticks(['team_name', 'team_clan_name', 'total_rounds_played'], ticks=parser.parse_event('round_end')['tick'])
    return df.loc[df['team_name'] == 'CT'].drop(columns=['team_name', 'tick', 'steamid', 'name']).drop_duplicates()['team_clan_name'].values
def get_ct_team_for_round(ct_teams: list[str], r: int):
    return ct_teams[r - 1]