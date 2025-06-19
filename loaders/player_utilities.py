from demoparser2 import DemoParser
from pandas import DataFrame

def get_utils_thrown(parser: DemoParser):
    # Get all instances of weapons fired
    df = parser.parse_event('weapon_fire')

    # Filter it to only contain utilities (for optimization purposes)
    df = df[df['weapon'].isin(['weapon_flashbang',
                               'weapon_smokegrenade',
                               'weapon_hegrenade',
                               'weapon_molotov',
                               'weapon_incgrenade'])]
    return df

def count_utils_thrown(df: DataFrame, player_name: str, round_start_tick: int, round_end_tick: int, weapon_name: str):
    # Simple filtering since everything is already set up
    filtered_df = df.loc[   (df['tick'] >= round_start_tick) &
                            (df['tick'] < round_end_tick) &
                            (df['user_name'] == player_name) &
                            (df['weapon'] == weapon_name)]
    return len(filtered_df)