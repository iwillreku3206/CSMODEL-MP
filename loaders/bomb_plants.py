import pandas as pd
from demoparser2 import DemoParser


def load_bomb_plants(parser: pd.DataFrame) -> pd.DataFrame:
    round_start_times = list(
        parser.parse_ticks(
            ["game_time"], ticks=parser.parse_event("round_freeze_end")["tick"]
        )
        .drop_duplicates(subset=["tick"])["tick"]
        .values
    ) + [parser.parse_ticks(["tick"]).iloc[-1]["tick"]]

    bomb_plants_df = parser.parse_event(
        "bomb_planted", player=["player_name", "team_name"]
    )

    if len(bomb_plants_df) == 0:
        return pd.DataFrame(columns=["round_id", "player_name"])

    # We create a column for round_id based on round start times
    bomb_plants_df["round_id"] = pd.cut(
        bomb_plants_df["tick"], bins=round_start_times, labels=False, right=True
    )

    bomb_plants_df = bomb_plants_df[["round_id", "user_name"]]

    bomb_plants_df.rename(
        columns={
            "user_name": "player_name",
        },
        inplace=True,
    )

    return bomb_plants_df


def get_bomb_planted(bomb_plants_df: pd.DataFrame, round_id: int, player_name: str) -> bool:
    filtered_df = bomb_plants_df[(bomb_plants_df["round_id"] == round_id) & (bomb_plants_df["player_name"] == player_name) ]
    return not filtered_df.empty
