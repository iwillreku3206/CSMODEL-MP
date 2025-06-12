from demoparser2 import DemoParser

def get_round_start_times(parser: DemoParser):
    return parser.parse_ticks(['game_time'],
                              ticks=parser.parse_event('round_freeze_end')['tick']
                              ).drop_duplicates(subset=['tick'])['game_time'].values
