import pandas as pd
from demoparser2 import DemoParser


def get_bomb_defuses(parser: DemoParser) -> pd.DataFrame:
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

    # We create a column for round_id based on round intervals
    bomb_defuse_df["round_id"] = pd.cut(
        bomb_defuse_df["tick"], bins=round_start_intervals, labels=False, right=True
    )

    bomb_defuse_df = bomb_defuse_df[["round_id", "user_name"]]

    return bomb_defuse_df


def is_bomb_defused(
    defuse_df: pd.DataFrame, round_id: int, player_name: str
) -> int:
    return not defuse_df[(defuse_df["user_name"] == player_name) & (defuse_df["round_id"] == round_id)].empty
