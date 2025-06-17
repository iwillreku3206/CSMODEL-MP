import pandas as pd
from demoparser2 import DemoParser


def get_player_kill_counts(parser: DemoParser) -> pd.DataFrame:
    # initialize data frame
    player_kills_df = parser.parse_event(
        "player_death",
        player=["last_place_name", "team_name"],
        other=["is_warmup_period", "tick"],
    )

    round_start_times = list(
        parser.parse_ticks(
            ["game_time"], ticks=parser.parse_event("round_freeze_end")["tick"]
        )
        .drop_duplicates(subset=["tick"])["tick"]
        .values
    ) + [parser.parse_ticks(["tick"]).iloc[-1]["tick"]]

    player_kills_df["round_id"] = pd.cut(
        player_kills_df["tick"], bins=round_start_times, labels=False, right=True
    )

    # filter out team-kills and warmup
    player_kills_df = player_kills_df[
        player_kills_df["attacker_team_name"] != player_kills_df["user_team_name"]
    ]

    player_kills_df = player_kills_df[player_kills_df["is_warmup_period"] == False]

    player_kills_df = (
        player_kills_df.groupby(["round_id", "attacker_name"])
        .size()
        .to_frame(name="kills")
        .reset_index()
    )

    # rename columns to match that of read_demo.py
    player_kills_df = player_kills_df.rename(
        columns={
            "attacker_name": "player_name",
            "kills": "player_kills",
        }
    )

    return player_kills_df


def get_player_kill_count(
    kill_counts_df: pd.DataFrame, round_id: int, player_name: str
) -> int:
    """
    Get the player kill count for each round.
    """

    filtered_df = kill_counts_df[
        (kill_counts_df["player_name"] == player_name)
        & (kill_counts_df["round_id"] == round_id)
    ]

    if filtered_df.empty:
        return 0
    else:
        return filtered_df["player_kills"].values[0]
