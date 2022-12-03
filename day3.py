from pathlib import Path

TEST_MODE = False


def phase1(rucksacks):
    return sum([score_rucksack(rucksack) for rucksack in rucksacks])


def score_rucksack(rucksack) -> int:
    return sum(map(lambda item: score_item(item), items_in_both(*compartments(rucksack))))


def phase2(v):
    elf_groups_of_3 = list(split(v, 3))
    badges = [item_in_all(group) for group in elf_groups_of_3]
    return sum([score_item(badge) for badge in badges])


def split(a_list: list, chunk_size: int) -> list:
    for i in range(0, len(a_list), chunk_size):
        yield a_list[i:i + chunk_size]


def item_in_all(rucksacks: list) -> str:
    a = items_in_both(set(rucksacks[0]), set(rucksacks[1]))
    return items_in_both(a, set(rucksacks[2])).pop()


def compartments(rucksack: str) -> tuple:
    mid = int(len(rucksack) / 2)
    return unpack_items(rucksack[:mid]), unpack_items(rucksack[mid:])


def unpack_items(s: str) -> set:
    return {*s}


def score_item(c: str) -> int:
    if c.islower():
        return ord(c) - ord('a') + 1
    else:
        return ord(c) - ord('A') + 27


def items_in_both(a: set, b: set) -> set:
    return a.union(b) - a ^ b


if __name__ == "__main__":
    with Path(__file__).parent.joinpath("input/day3_sample" if TEST_MODE else "input/day3").open() as f:
        values = [i.strip() for i in f]
        print(f'Phase 1: {phase1(values)}')
        print(f'Phase 2: {phase2(values)}')
