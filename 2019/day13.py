import dataclasses
from copy import deepcopy
from pathlib import Path

from computer import Computer

TEST_MODE = True


@dataclasses.dataclass
class Coord:
    x: int
    y: int


@dataclasses.dataclass
class Game:
    computer: Computer
    screen: dict
    num_blocks: int = 0
    paddle = None
    ball = None
    score = None

    def start(self):
        outputs = self.computer.compute([])
        self.read_outputs(outputs)
        self.num_blocks = len([tile for tile in self.screen.values() if tile == 2])

    def move(self, direction):
        outputs = self.computer.compute([direction])
        self.read_outputs(outputs)

    def read_outputs(self, outputs):
        for i in range(0, len(outputs) - 2, 3):
            x, y, tile = outputs[i], outputs[i + 1], outputs[i + 2]
            if x == -1 and y == 0:
                self.score = tile
            else:
                if tile == 0 and (x, y) in self.screen and self.screen[(x, y)] == 2:
                    self.num_blocks -= 1

                self.screen[(x, y)] = tile
                if tile == 4:
                    self.ball = Coord(x, y)
                if tile == 3:
                    self.paddle = Coord(x, y)

    def print(self):
        for y in range(23):
            for x in range(35):
                if (x, y) not in self.screen:
                    print(' ', end='')
                elif self.screen[(x, y)] == 1:
                    print('#', end='')
                elif self.screen[(x, y)] == 2:
                    print('B', end='')
                elif self.screen[(x, y)] == 3:
                    print(f"{self.paddle.x}", end='')
                elif self.screen[(x, y)] == 4:
                    print(f"{self.ball.x}", end='')
                else:
                    print('.', end='')
            print('')


def phase1(code):
    game = Game(Computer(code), {})
    game.start()
    return game.num_blocks


def phase2(code):
    code[0] = 2
    game = Game(Computer(code), {})
    game.start()
    target_x = project(game)

    while game.num_blocks > 0:
        prev_ball_pos = game.ball
        direction = 1 if target_x > game.paddle.x else -1 if target_x < game.paddle.x else 0
        game.move(direction)
        ball_rising = game.ball.y <= prev_ball_pos.y

        if ball_rising and game.paddle.y - game.ball.y == 2:
            target_x = project(game)

    return game.score


def project(game):
    projection = deepcopy(game)

    if projection.ball.y >= projection.paddle.y - 1:
        return None

    while projection.ball.y < projection.paddle.y - 1 and projection.num_blocks > 0:
        projection.move(0)

    return projection.ball.x


if __name__ == "__main__":
    with Path(__file__).parent.joinpath("input/day13_sample" if TEST_MODE else "input/day13").open() as f:
        values = [int(x) for x in [i.split(',') for i in f][0]]
        print(f'Phase 1: {phase1(values)}')
        print(f'Phase 2: {phase2(values)}')
