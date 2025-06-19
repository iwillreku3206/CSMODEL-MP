from demoparser2 import DemoParser
from pandas import DataFrame

def get_all_loadouts_at_round_freeze_end(parser: DemoParser, round_freeze_end_ticks: []):
    loadout_df = parser.parse_ticks(['inventory'])
    loadout_df = loadout_df[loadout_df['tick'].isin(round_freeze_end_ticks)]

    return loadout_df

def get_player_loadout_at_round_freeze_end(loadout_df: DataFrame, player_name: str, round_freeze_end_tick: int):
    player_loadout_df = loadout_df.loc[(loadout_df['tick'] == round_freeze_end_tick) &
                         (loadout_df['name'] == player_name)]['inventory']

    return player_loadout_df