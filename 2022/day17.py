from pathlib import Path
import collections

TEST_MODE = False

Coord = collections.namedtuple("Coord", "x y")
Sprite = collections.namedtuple("Sprite", "coords width, height")
ActiveSprite = collections.namedtuple("Sprite", "sprite loc")

sprite_1 = Sprite([Coord(0, 0), Coord(1, 0), Coord(2, 0), Coord(3, 0)], 4, 1)
sprite_2 = Sprite([Coord(1, 1), Coord(2, 1), Coord(0, 1), Coord(1, 0), Coord(1, 2)], 3, 3)
sprite_3 = Sprite([Coord(0, 0), Coord(2, 0), Coord(2, 1), Coord(1, 0), Coord(2, 2)], 3, 3)
sprite_4 = Sprite([Coord(0, 0), Coord(0, 1), Coord(0, 2), Coord(0, 3)], 1, 4)
sprite_5 = Sprite([Coord(0, 1), Coord(1, 0), Coord(0, 0), Coord(1, 1)], 2, 2)

sprites = [sprite_1, sprite_2, sprite_3, sprite_4, sprite_5]


def phase1(gas_pattern):
    highest, _ = simulation(2022, gas_pattern)
    return highest


def phase2(gas_pattern):
    last = 0
    for i in range(3, 1000, 10):
        highest, rocks = simulation(i, gas_pattern)
        print(highest - last)
    print(f"{highest} {len(rocks)}")
    hashes = {}
    for i in range(len(rocks)):
        pile = rocks[i:1000 + i]
        exes = [c.x for c in pile]
        the_hash = hash(tuple(exes))
        if the_hash in hashes:
            print(f"{i} {hashes[the_hash]}")
        else:
            hashes[the_hash] = i
    return -1


def print_screen(current_sprite, rocks):
    height = current_sprite.loc.y + current_sprite.sprite.height
    for y in range(height, max(0, height-15), -1):
        print('|', end='')
        for x in range(7):
            if Coord(x, y) in [Coord(c.x + current_sprite.loc.x, c.y + current_sprite.loc.y) for c in current_sprite.sprite.coords]:
                print('@', end='')
            elif Coord(x, y) in rocks:
                print('#', end='')
            else:
                print('.', end='')
        print('')
    print('---------')


def simulation(finished, gas_pattern):
    rocks = []
    current_sprite = None
    dropped = 0
    sprite = sprite_generator()
    highest_rock = 0
    for blast in next_gas_blast(gas_pattern):
        if current_sprite is None:
            current_sprite = start_sprite(next(sprite), highest_rock)

        current_sprite = gas_blast(current_sprite, blast, rocks, highest_rock)

        if sprite_touching_rocks(current_sprite, rocks, down, highest_rock):
            highest_rock = sprite_to_rocks(current_sprite, rocks, highest_rock)
            dropped += 1
            current_sprite = None
            if dropped >= finished:
                return highest_rock, rocks
        else:
            current_sprite = ActiveSprite(current_sprite.sprite, Coord(current_sprite.loc.x, current_sprite.loc.y - 1))


def sprite_generator():
    for i in range(100000000):
        yield sprites[i % 5]


def next_gas_blast(gas_pattern):
    size = len(gas_pattern)
    for i in range(1000000000):
        yield gas_pattern[i % size]


def start_sprite(sprite, highest_rock):
    return ActiveSprite(sprite, Coord(2, highest_rock + 4))


def to_left(rock, pixel):
    return rock.y == pixel.y and pixel.x - rock.x == 1


def to_right(rock, pixel):
    return rock.y == pixel.y and rock.x - pixel.x == 1


def down(rock, pixel):
    return rock.x == pixel.x and pixel.y - rock.y == 1


def sprite_touching_rocks(active_sprite, rocks, func, highest_rock):
    lowest_sprite_y = active_sprite.loc.y
    if lowest_sprite_y - highest_rock > 1:
        return False
    if func is down and lowest_sprite_y == 1:
        return True
    for coord in active_sprite.sprite.coords:
        x = active_sprite.loc.x + coord.x
        y = active_sprite.loc.y + coord.y
        for rock in rocks[-100:]:
            if func(rock, Coord(x, y)):
                return True
    return False


def gas_blast(active_sprite, blast, rocks, highest_rock):
    if blast == '>' and active_sprite.loc.x + active_sprite.sprite.width < 7 and not sprite_touching_rocks(active_sprite, rocks, to_right, highest_rock):
        x = active_sprite.loc.x + 1
    elif blast == '<' and active_sprite.loc.x > 0 and not sprite_touching_rocks(active_sprite, rocks, to_left, highest_rock):
        x = active_sprite.loc.x - 1
    else:
        x = active_sprite.loc.x
    return ActiveSprite(active_sprite.sprite, Coord(x, active_sprite.loc.y))


def sprite_to_rocks(active_sprite, rocks, highest_rock):
    sprite_coords = [Coord(active_sprite.loc.x + coord.x, active_sprite.loc.y + coord.y) for coord in
                     active_sprite.sprite.coords]
    rocks.extend(sprite_coords)
    return max(highest_rock, rocks[-1].y)


if __name__ == "__main__":
    with Path(__file__).parent.joinpath("input/day17_sample" if TEST_MODE else "input/day17").open() as f:
        values = [i for i in f][0]
        print(f'Phase 1: {phase1(values)}')
        print(f'Phase 2: {phase2(values)}')
