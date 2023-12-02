import collections
from pathlib import Path

TEST_MODE = False

Draw = collections.namedtuple('Draw', ('red', 'green', 'blue'))
Game = collections.namedtuple('Game', ('id', 'draws'))


def phase1(games):
    return sum([game.id for game in games if is_game_valid(game, red=12, green=13, blue=14)])


def phase2(games):
    return sum([draw_power(game) for game in games])


def draw_power(game):
    green = max([draw.green for draw in game.draws])
    blue = max([draw.red for draw in game.draws])
    red = max([draw.blue for draw in game.draws])
    return green * red * blue


def is_game_valid(game: Game, red: int, green: int, blue: int):
    valid_draws = [draw for draw in game.draws if is_draw_valid(draw, red, green, blue)]
    return len(valid_draws) == len(game.draws)


def is_draw_valid(draw: Draw, red: int, green: int, blue: int):
    return draw.red <= red and draw.green <= green and draw.blue <= blue


def parse_game(line):
    def draw(_d):
        green = red = blue = 0
        for d in _d:
            if d[1] == 'green':
                green += int(d[0])
            if d[1] == 'blue':
                blue += int(d[0])
            if d[1] == 'red':
                red += int(d[0])
        return Draw(red=red, green=green, blue=blue)
    a, b = line.split(':')
    game_num = int(a[5:])
    return Game(game_num, [draw([x.strip().split(' ') for x in a.split(',')]) for a in b.split(";")])


if __name__ == "__main__":
    with Path(__file__).parent.joinpath("input/day2_sample" if TEST_MODE else "input/day2").open() as f:
        values = [parse_game(i.strip()) for i in f]
        print(f'Phase 1: {phase1(values)}')
        print(f'Phase 2: {phase2(values)}')
