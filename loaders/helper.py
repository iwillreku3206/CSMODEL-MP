from demoparser2 import DemoParser

def get_round_start_ticks(parser: DemoParser):
    round_start_ticks = parser.parse_event('round_officially_ended').drop_duplicates()
    round_start_ticks = round_start_ticks['tick'].tolist()

    # Add 0 at the start and an arbitrary number at the end for later parsing purposes
    round_start_ticks.insert(0, 0)
    round_start_ticks.append(9_999_999)

    return round_start_ticks

def get_round_freeze_end_ticks(parser: DemoParser):
    return parser.parse_event('round_freeze_end')['tick'].tolist()