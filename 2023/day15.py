import collections
import dataclasses
from pathlib import Path

TEST_MODE = False

Instruction = collections.namedtuple("Instruction", "label, type, box, focal")
Lens = collections.namedtuple("Lens", "label, focal")


@dataclasses.dataclass
class Box:
    box_number: int
    lenses: list

    def add_lens(self, label, focal):
        val = next((index for index, lens in enumerate(self.lenses) if lens.label == label), None)
        if val is None:
            self.lenses.append(Lens(label, focal))
        else:
            current = self.lenses[val]
            self.lenses[val] = Lens(current.label, focal)

    def remove_lens(self, label):
        self.lenses = [lens for lens in self.lenses if lens.label != label]

    def focus_power(self):
        acc = 0
        for index, lens in enumerate(self.lenses):
            acc += (1 + self.box_number) * (1 + index) * lens.focal
        return acc


def phase1(v):
    return sum([decode(c) for c in v])


def phase2(v):
    instructions = [read_instruction(s) for s in v]
    boxes = {}
    for i in range(0, 256):
        boxes[i] = Box(i, [])

    for instruction in instructions:
        box = boxes[instruction.box]
        if instruction.type == 'add':
            box.add_lens(instruction.label, instruction.focal)
        else:
            box.remove_lens(instruction.label)

    return sum([b.focus_power() for b in boxes.values()])


def read_instruction(s):
    x = s.split('=')
    if len(x) == 1:
        label = x[0][0:-1]
        return Instruction(label, 'remove', decode(label), None)
    label, b = x
    return Instruction(label, 'add', decode(label), int(b))


def decode(code):
    current = 0
    for c in code:
        current += ord(c)
        current *= 17
        current = current % 256
    return current


if __name__ == "__main__":
    with Path(__file__).parent.joinpath("input/day15_sample" if TEST_MODE else "input/day15").open() as f:
        values = [i.strip() for i in f][0].split(',')
        print(f'Phase 1: {phase1(values)}')
        print(f'Phase 2: {phase2(values)}')
