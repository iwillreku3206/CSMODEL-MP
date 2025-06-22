import pandas as pd
from demoparser2 import DemoParser


def get_bomb_defuses(parser: DemoParser, round_start_times_df: pd.DataFrame) -> pd.DataFrame:
    round_start_intervals = list(
        parser.parse_ticks(
            ["game_time"], ticks=parser.parse_event("round_freeze_end")["tick"]
        )
        .drop_duplicates(subset=["tick"])["tick"]
        .values
    ) + [parser.parse_ticks(["tick"]).iloc[-1]["tick"]]

    bomb_defuse_df = parser.parse_event(
        "bomb_defused", player=["player_name", "team_name"]
    )

    if len(bomb_defuse_df) == 0:
        return pd.DataFrame({"round_id": [], "user_name": [], "time": []})

    offset = 0

    # get times of tick
    ticks = parser.parse_ticks(['game_time'], ticks=(bomb_defuse_df['tick'] - offset)).drop_duplicates(subset='tick')[['game_time', 'tick']]
    ticks['tick'] += offset
    bomb_defuse_df = pd.merge(bomb_defuse_df, ticks, on="tick", how="inner")


    # We create a column for round_id based on round intervals
    bomb_defuse_df["round_id"] = pd.cut(
        bomb_defuse_df["tick"], bins=round_start_intervals, labels=False, right=True
    )

    # merge with round start times
    bomb_defuse_df['round_for_calc'] = bomb_defuse_df['round_id'] + 1 # defuse happens on next round
    bomb_defuse_df = pd.merge(bomb_defuse_df, round_start_times_df, left_on="round_id", right_on=['total_rounds_played'], how="inner")
    bomb_defuse_df["time"] = bomb_defuse_df['game_time'] - bomb_defuse_df['round_start_time']

    bomb_defuse_df = bomb_defuse_df[["round_id", "user_name", "time"]]

    return bomb_defuse_df


def is_bomb_defused(
    defuse_df: pd.DataFrame, round_id: int, player_name: str
) -> int:
    return not defuse_df[(defuse_df["user_name"] == player_name) & (defuse_df["round_id"] == round_id)].empty

def bomb_defuse_time(defuse_df: pd.DataFrame, round_id: int):
    v = defuse_df.loc[defuse_df['round_id'] == round_id]['time'].values
    if len(v) == 0:
        return None
    else:
        return v[0]
