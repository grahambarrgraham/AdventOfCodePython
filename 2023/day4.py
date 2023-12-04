import collections
import re
from pathlib import Path

TEST_MODE = False

Card = collections.namedtuple("card", "id, winners, numbers")


def phase1(cards: list[Card]):
    card_scores = [score(find_winners(card)) for card in cards]
    return sum(card_scores)


def phase2(cards: list[Card]):
    card_id_copies: dict[int, int] = dict()
    card_winner_counts: dict[int, int] = {card.id: len(find_winners(card)) for card in cards}
    for card in cards:
        card_id_copies[card.id] = 1
    for card in cards:
        for next_card_id in range(card.id + 1, card.id + 1 + card_winner_counts[card.id]):
            if next_card_id <= len(cards):
                card_id_copies[next_card_id] += card_id_copies[card.id]
    return sum(card_id_copies.values())


def find_winners(card):
    return [number for number in card.numbers if number in card.winners]


def score(winners):
    if len(winners) == 0:
        return 0
    result = 1
    for _ in range(len(winners) - 1):
        result *= 2
    return result


def parse_line(line):
    m = re.match("^Card\s+(\d+)\\: (.+) \\| (.+)", line)
    card_num = int(m.group(1))
    winners = {int(winner.strip()) for winner in m.group(2).strip().split(' ') if winner != ''}
    numbers = [int(number.strip()) for number in m.group(3).strip().split(' ') if number != '']
    return Card(card_num, winners, numbers)


if __name__ == "__main__":
    with Path(__file__).parent.joinpath("input/day4_sample" if TEST_MODE else "input/day4").open() as f:
        values = [parse_line(i.strip()) for i in f]
        print(f'Phase 1: {phase1(values)}')
        print(f'Phase 2: {phase2(values)}')
