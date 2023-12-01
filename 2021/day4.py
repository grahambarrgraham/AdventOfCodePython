from pathlib import Path
import sys

TEST_MODE = bool(len(sys.argv) > 1 and sys.argv[1] == "test")


def phase1(boards, numbers):
    for number in numbers:
        for board in boards:
            board.set_number(number)
            if board.has_won():
                return board.sum() * number
    return -1


def phase2(boards, numbers):
    target = len(boards)
    winners = set()
    for number in numbers:
        boards = [board for board in boards if board not in winners]
        for board in boards:
            board.set_number(number)
            if board.has_won():
                winners.add(board)
                if len(winners) == target:
                    return board.sum() * number
    return -1


class Board:
    def __init__(self, board):
        self.board = board

    def set_number(self, number):
        for j in range(len(self.board)):
            for i in range(len(self.board)):
                if self.board[i][j] == number:
                    self.board[i][j] = -1

    def has_won(self):
        for row in self.board:
            if sum(row) == -1 * len(self.board):
                return True

        for i in range(len(self.board)):
            if sum([row[i] for row in self.board]) == -1 * len(self.board):
                return True

        return False

    def sum(self):
        return sum([sum([num for num in row if num > -1]) for row in self.board])


def load(data):
    numbers = [int(num) for num in data.pop(0)[0].split(',')]
    boards = [Board([[int(num) for num in row.split()] for row in raw]) for raw in data]
    return numbers, boards


if __name__ == "__main__":
    with Path(__file__).parent.joinpath("input/day4_sample" if TEST_MODE else "input/day4").open() as f:
        NUMBERS, BOARDS = load([line.split("\n") for line in f.read().split("\n\n")])
        print(f'Phase 1: {phase1(BOARDS, NUMBERS)}')
        print(f'Phase 2: {phase2(BOARDS, NUMBERS)}')
