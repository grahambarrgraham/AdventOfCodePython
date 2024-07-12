from pathlib import Path

TEST_MODE = False


def phase1(v):
    fuel = [m // 3 - 2 for m in v]
    return sum(fuel)


def phase2(v):
    fuel = [calc_fuel_mass(m) for m in v]
    return sum(fuel)


def calc_fuel_mass(mass):
    fuel_mass = mass // 3 - 2
    return fuel_mass + calc_fuel_mass(fuel_mass) if fuel_mass > 0 else 0


if __name__ == "__main__":
    with Path(__file__).parent.joinpath("input/day1_sample" if TEST_MODE else "input/day1").open() as f:
        values = [int(i) for i in f]
        print(f'Phase 1: {phase1(values)}')
        print(f'Phase 2: {phase2(values)}')


