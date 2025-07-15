import pandas as pd
import numpy as np

#  load csvs of demos, players, and teams
demos = pd.read_csv("demos.csv")
players = pd.read_csv("players.csv")
teams = pd.read_csv("teams.csv")

# clean player names
players['name'] = players['name'].replace('910', '910-')
players['name'] = players['name'].replace('HeavyGod', 'HeavyGoD')
players['name'] = players['name'].replace('mzinho', 'Mzinho')
players['name'] = players['name'].replace('skullz', 'Skullz')
players['name'] = players['name'].replace('Techno', 'Techno4K')
players['name'] = players['name'].replace('Westmelon', 'westmelon')
players['name'] = players['name'].replace('z4kr', 'z4KR')
# clean team names
teams['team_name'] = teams['team_name'].replace('BC.Game', 'BCG')
teams['team_name'] = teams['team_name'].replace('FaZe', 'FaZe Clan')
teams['team_name'] = teams['team_name'].replace('Falcons', 'Team Falcons')
teams['team_name'] = teams['team_name'].replace('G2', 'G2 Esports')
teams['team_name'] = teams['team_name'].replace('Legacy', 'LEGACY')
teams['team_name'] = teams['team_name'].replace('Liquid', 'Team Liquid')
teams['team_name'] = teams['team_name'].replace('Lynn Vision', 'Lynn Vision Gaming')
teams['team_name'] = teams['team_name'].replace('Vitality', 'Team Vitality')

# convert debut month to int
players['proplayer_since_month'] = players['proplayer_since_month'].apply(lambda x: pd.to_datetime(x, format='%B').month)
players['proplayer_since_year'] = players['proplayer_since_year'].astype(int)
# convert debut current team to int
players['on_team_since_month'] = players['on_team_since_month'].apply(lambda x: pd.to_datetime(x, format='%B').month)
players['on_team_since_year'] = players['on_team_since_year'].astype(int)

# caclulate months from player's debut month and year to May 2025 when IEM Dallas was played
players['career_length'] = (2025 - players['proplayer_since_year']) * 12 + (5 - players['proplayer_since_month'])
players['curr_team_length'] = (2025 - players['on_team_since_year']) * 12 + (5 - players['on_team_since_month'])
players.rename(columns={'name': 'player_name'}, inplace=True)
players = players[['player_name', 'career_length', 'curr_team_length']]

# perform joins
demos = pd.merge(demos,players,on='player_name',how='inner')
demos = pd.merge(demos, teams, on='team_name', how='inner')