import re
from pathlib import Path
from collections import namedtuple
from math import ceil

TEST_MODE = True

Blueprint = namedtuple("BluePrint", "id, ore_ore, clay_ore, obsidian_ore, obsidian_clay, geode_ore, geode_obsidian")


def phase1(v):
    # print([calc_max_geodes(blueprint) for blueprint in v])
    print(calc_max_geodes(v[1]))


def calc_max_geodes(blueprint: Blueprint) -> int:
    ore_bots = 1
    clay_bots = 0
    obsidian_bots = 0
    geode_bots = 0
    ore = 0
    clay = 0
    obsidian = 0
    geodes = 0

    for minute in range(1, 25):
        building_geode_bots = 0
        building_obsidian_bots = 0
        building_clay_bots = 0
        building_ore_bots = 0
        print(f"== Minute {minute} ==")

        minutes_till_clay_bot = 25 if clay_bots == 0 else ceil((blueprint.clay_ore - ore) / clay_bots)
        minutes_till_obsidian_bot = 25 if clay_bots == 0 or ore_bots == 0 \
            else ceil(max((blueprint.obsidian_clay - clay) / clay_bots, (blueprint.obsidian_ore - ore) / ore_bots))
        minutes_till_geode_bot = 25 if obsidian_bots == 0 or ore_bots == 0 else \
            ceil(max((blueprint.geode_obsidian - obsidian) / obsidian_bots, (blueprint.geode_ore - ore) / ore_bots))

        print(f"minutes to obsidian {minutes_till_obsidian_bot}")

        if obsidian >= blueprint.geode_obsidian and ore >= blueprint.geode_ore:
            building_geode_bots += 1
            ore -= blueprint.geode_ore
            obsidian -= blueprint.geode_obsidian
            print(f"Spend {blueprint.geode_ore} ore and {blueprint.geode_obsidian} obsidian to build geode "
                  f"cracking robot")
        elif clay >= blueprint.obsidian_clay and ore >= blueprint.obsidian_ore:
            if minutes_till_geode_bot < 3:
                print(f"Could build obsidian robot, but waiting {minutes_till_geode_bot} minutes to build geode")
            else:
                building_obsidian_bots += 1
                ore -= blueprint.obsidian_ore
                clay -= blueprint.obsidian_clay
                print(f"Spend {blueprint.obsidian_ore} ore and {blueprint.obsidian_clay} clay to build obsidian "
                      f"collecting robot")
        elif ore >= blueprint.clay_ore:
            if minutes_till_obsidian_bot < 3:
                print(f"Could build clay robot, but waiting {minutes_till_obsidian_bot} minutes to build obsidian")
            else:
                building_clay_bots += 1
                ore -= blueprint.clay_ore
                print(f"Spend {blueprint.clay_ore} ore to build clay collecting robot")
        elif ore >= blueprint.ore_ore:
            building_ore_bots += 1
            ore -= blueprint.ore_ore
            print(f"Spend {blueprint.ore_ore} to build ore collecting robot")

        ore += ore_bots
        print(f"{ore_bots} ore collected, now have {ore}")
        clay += clay_bots
        if clay_bots > 0:
            print(f"{clay_bots} clay collected, now have {clay}")
        obsidian += obsidian_bots
        if obsidian_bots > 0:
            print(f"{obsidian_bots} obsidian collected, now have {obsidian}")
        geodes += geode_bots
        if geode_bots > 0:
            print(f"{geode_bots} geodes cracked, now have {geodes}")

        ore_bots += building_ore_bots
        clay_bots += building_clay_bots
        obsidian_bots += building_obsidian_bots
        geode_bots += building_geode_bots
        print(f"Now have {ore_bots}, {clay_bots}, {obsidian_bots}, {geode_bots}")
        print()

    return geodes


def phase2(v):
    return -1


def parse(line):
    pattern = re.compile("Blueprint (.+): Each ore robot costs (.+) ore. Each clay robot costs (.+) ore. Each "
                         "obsidian robot costs (.+) ore and (.+) clay. Each geode robot costs (.+) ore and (.+) "
                         "obsidian.")
    m = pattern.match(line)
    return Blueprint(int(m.group(1)), int(m.group(2)), int(m.group(3)), int(m.group(4)), int(m.group(5)),
                     int(m.group(6)), int(m.group(7)))


if __name__ == "__main__":
    with Path(__file__).parent.joinpath("input/day19_sample" if TEST_MODE else "input/day19").open() as f:
        values = [parse(i) for i in f]
        print(f'Phase 1: {phase1(values)}')
        print(f'Phase 2: {phase2(values)}')


