import pandas as pd
from demoparser2 import DemoParser


def player_shots_all(
    parser: DemoParser,
    part: str,
) -> pd.DataFrame | None:
    """
    ChatGPT was used to assist in understanding dataframe manipulation techniques in Pandas, particularly with .
    Much of the actual code following was written by Sean Bernardo.


    Inspecting the demo we get the following hitgroups: ['generic', 'head', 'chest', 'left_arm', 'stomach', 'right_arm', 'left_leg', 'right_leg', 'neck']

    Groupings are determined by testing damage done to each hitgroup.

    The following console commands were used to determine damage applied and aim specific hitbox groups:
        player_debug_print_damage true
        cl_ent_hitbox *

    Each hitbox group was tested 5 times and the average damage was recorded rounded to the nearest integer.

    Head:       205

    Upper Body
    - Neck:      48
    - Chest:     48
    - Right Arm: 48
    - Left Arm:  48

    - Stomach:   60

    Legs
    - Right Leg: 38
    - Left Leg:  38

    We drop generic as this usually covers fall damage and utils
    """

    player_shots_df = parser.parse_event("player_hurt")

    # This I robbed get_round_start_times which is rinaldo's code but instead i change it to tick so no need for more conversions
    # because of how bins work, we add the last tick of the demo to accommodate the last round
    round_start_times = list(
        parser.parse_ticks(
            ["game_time"], ticks=parser.parse_event("round_freeze_end")["tick"]
        )
        .drop_duplicates(subset=["tick"])["tick"]
        .values
    ) + [parser.parse_ticks(["tick"]).iloc[-1]["tick"]]

    # We create a surrogate column for round_id based on round start times
    player_shots_df["round_id"] = pd.cut(
        player_shots_df["tick"], bins=round_start_times, labels=False, right=True
    )

    hitgroups = {
        "head": ["head"],
        "upperbody": ["neck", "chest", "right_arm", "left_arm"],
        "stomach": ["stomach"],
        "legs": ["right_leg", "left_leg"],
    }

    if part not in hitgroups:
        return

    player_shots_df = player_shots_df[player_shots_df["hitgroup"].isin(hitgroups[part])]

    player_shots_df = (
        player_shots_df.groupby(["round_id", "attacker_name"])
        .size()
        .reset_index(name=f"player_{part}shots")
    )

    player_shots_df = (
        player_shots_df.rename(
            columns={
                "attacker_name": "player_name",
            }
        )
        .sort_values(by=["round_id", "player_name"])
        .reset_index(drop=True)
    )

    return player_shots_df


def get_player_shots(
    shots_df: pd.DataFrame,
    part: str,
    round_id: int,
    player_name: str,
) -> int | None:

    filtered_df = shots_df[
        (shots_df["player_name"] == player_name) & (shots_df["round_id"] == round_id)
    ]

    if filtered_df.empty:
        return 0
    else:
        return filtered_df[f"player_{part}shots"].values[0]
