import dataclasses
import functools
from pathlib import Path

TEST_MODE = False

all_cards_v1 = ['A', 'K', 'Q', 'J', 'T', '9', '8', '7', '6', '5', '4', '3', '2']
all_cards_v2 = ['A', 'K', 'Q', 'T', '9', '8', '7', '6', '5', '4', '3', '2', 'J']
card_rank_v1 = {c: i + 1 for i, c in enumerate(reversed(all_cards_v1))}
card_rank_v2 = {c: i + 1 for i, c in enumerate(reversed(all_cards_v2))}
hand_types = ['FIVE', 'FOUR', 'FH', 'THREE', 'TWO_PAIRS', 'PAIR', 'HIGH']
hand_type_rank = {t: n + 1 for n, t in enumerate(reversed(hand_types))}


@dataclasses.dataclass(frozen=True)
class Hand:
    cards: str
    bid: int = 0

    def hand_type_rank(self, preprocess) -> int:
        cards = preprocess(self.cards)
        return hand_type_rank[self.hand_type(cards)]

    @staticmethod
    def hand_type(cards: str) -> str:
        unique_cards = {c for c in cards}
        card_group_sizes = [len([n for n in cards if n == c]) for c in unique_cards]
        card_group_sizes.sort(reverse=True)
        if card_group_sizes[0] == 5:
            return 'FIVE'
        if card_group_sizes[0] == 4:
            return 'FOUR'
        if card_group_sizes[0] == 3 and card_group_sizes[1] == 2:
            return 'FH'
        if card_group_sizes[0] == 3:
            return 'THREE'
        if card_group_sizes[0] == 2 and card_group_sizes[1] == 2:
            return 'TWO_PAIRS'
        if card_group_sizes[0] == 2:
            return 'PAIR'
        return 'HIGH'


def phase1(hands: list[Hand]):
    return process(hands, compare_v1)


def phase2(hands: list[Hand]):
    return process(hands, compare_v2)


def compare(card_rank, pre, a: Hand, b: Hand):
    if a.hand_type_rank(pre) > b.hand_type_rank(pre):
        return 1
    if a.hand_type_rank(pre) < b.hand_type_rank(pre):
        return -1
    for i, card_a in enumerate(a.cards):
        card_b = b.cards[i]
        if card_rank[card_a] > card_rank[card_b]:
            return 1
        if card_rank[card_a] < card_rank[card_b]:
            return -1
    return 0


def compare_v1(a: Hand, b: Hand):
    return compare(card_rank_v1, lambda k: k, a, b)


def compare_v2(a: Hand, b: Hand):
    return compare(card_rank_v2, process_js, a, b)


def process_js(cards: str):
    num_js = len([c for c in cards if c == 'J'])
    if num_js == 0 or num_js == 5:
        return cards
    unique_cards = {c for c in cards if c != 'J'}
    c = [Hand(cards.replace('J', uc), 0) for uc in unique_cards]
    c.sort(key=functools.cmp_to_key(compare_v1), reverse=True)
    return c[0].cards


def process(hands, v_):
    hands.sort(key=functools.cmp_to_key(v_))
    hand_scores = [(rank + 1) * hand.bid for rank, hand in enumerate(hands)]
    return sum(hand_scores)


def parse_hand(param):
    return Hand(param[0], int(param[1]))


if __name__ == "__main__":
    with Path(__file__).parent.joinpath("input/day7_sample" if TEST_MODE else "input/day7").open() as f:
        values = [parse_hand(i.strip().split()) for i in f]
        print(f'Phase 1: {phase1(values)}')
        print(f'Phase 2: {phase2(values)}')
