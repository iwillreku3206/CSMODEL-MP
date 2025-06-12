from demoparser2 import DemoParser

def get_game_time_offset(parser: DemoParser):
    parser.parse_ticks(['game_time'], ticks=[1])['game_time'].values[0]