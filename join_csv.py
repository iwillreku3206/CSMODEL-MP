import pandas as pd

"""
Individual match files are named in the format:
<match_id>_<map_id>.dem.csv

Files must also be stored in the "csv" directory relative to this script.
"""

matches_maps_ids = (
    (0, 0),
    (0, 1),
    (1, 2),
    (1, 3),
    (1, 4),
    (2, 5),
    (2, 6),
    (3, 7),
    (3, 8),
    (4, 9),
    (4, 10),
    (5, 11),
    (5, 12),
    (6, 13),
    (6, 14),
    (7, 15),
    (7, 16),
    (7, 17),
    (8, 18),
    (8, 19),
    (9, 20),
    (9, 21),
    (9, 22),
    (10, 23),
    (10, 24),
    (11, 25),
    (11, 26),
    (12, 27),
    (12, 28),
    (13, 29),
    (13, 30),
    (13, 31),
    (14, 32),
    (14, 33),
    (15, 34),
    (15, 35),
    (16, 36),
    (16, 37),
    (17, 38),
    (17, 39),
    (17, 40),
    (18, 41),
    (18, 42),
    (18, 43),
    (19, 44),
    (19, 45),
    (19, 46),
    (20, 47),
    (20, 48),
    (21, 49),
    (21, 50),
    (21, 51),
    (22, 52),
    (22, 53),
    (22, 54),
    (23, 55),
    (23, 56),
    (23, 57),
    (24, 58),
    (24, 59),
    (25, 60),
    (25, 61),
    (25, 62),
    (26, 63),
    (26, 64),
    (27, 65),
    (27, 66),
    (27, 67),
    (28, 68),
    (28, 69),
    (28, 70),
)

df_composite = pd.DataFrame()

num_rounds = 0

for match_id, map_id in matches_maps_ids:
    file_name = f"{match_id:02d}_{map_id:02d}.dem.csv"

    try:
        df_match = pd.read_csv("csv/" + file_name)
        df_match["round_id"] = df_match["round_number"] + num_rounds - 1  # 0 indexing

        round_ids = list(map(int, df_match["round_id"].unique()))
        map_rounds = len(round_ids)
        
        print(f"Parsing {file_name}: {map_rounds} rounds")
        
        df_composite = pd.concat([df_composite, df_match])
        num_rounds += map_rounds
    except FileNotFoundError:
        print(f"{file_name} not found. Skipping.")
        continue
    except Exception as e:
        print(f"File error: {e}")
        continue

df_composite.to_csv("IEM_DALLAS_2025.csv", index=False)
