from pathlib import Path
import re
import collections

TEST_MODE = False

Token = collections.namedtuple('Token', ('kind', 'value'))
Directory = collections.namedtuple('Directory', ('size', 'children'))


def phase1(v):
    fully_sized_dirs = recurse_size(to_directory_map(list(tokenize(v))))
    return sum([d for d in fully_sized_dirs.values() if d < 100000])


def phase2(v):
    fully_sized_dirs = recurse_size(to_directory_map(list(tokenize(v))))
    required = 30000000 - (70000000 - fully_sized_dirs['/'])
    return min([d for d in fully_sized_dirs.values() if d > required])


def recurse_size(dirs):
    fully_sized_dirs = {}
    for d in dirs.keys():
        fully_sized_dirs[d] = calc_dir_size(d, dirs, fully_sized_dirs)
    return fully_sized_dirs


def child_name(parent, child):
    return parent + '/' + child if parent != '/' and child != '/' else parent + child


def calc_dir_size(directory, dirs, fully_sized_dirs):
    if directory in fully_sized_dirs:
        return fully_sized_dirs[directory]
    size = dirs[directory].size + sum([calc_dir_size(child_name(directory, child), dirs, fully_sized_dirs)
                                       for child in dirs[directory].children])
    fully_sized_dirs[directory] = size
    return size


def to_directory_map(tokens):
    current_dir = ''
    size = 0
    children = []
    dirs = {}
    for token in tokens:
        match token.kind:
            case 'CD':
                if current_dir not in dirs:
                    dirs[current_dir] = Directory(size, children)
                if token.value == '..':
                    current_dir = current_dir[:current_dir.rfind('/')]
                else:
                    current_dir = child_name(current_dir, token.value)
            case 'FILE':
                size += token.value
            case 'DIR':
                children.append(token.value)
            case 'LS':
                size = 0
                children = []
    dirs[current_dir] = Directory(size, children)
    return dirs


def tokenize(lines):
    pattern = re.compile(r'(\$ ls)|(\d+) .+|dir (.+)|\$ cd (.+)')
    for line in lines:
        mo = pattern.fullmatch(line)
        match mo.lastindex:
            case 1:
                tok = Token('LS', '')
            case 2:
                tok = Token('FILE', int(mo.group(mo.lastindex)))
            case 3:
                tok = Token('DIR', mo.group(mo.lastindex))
            case 4:
                tok = Token('CD', mo.group(mo.lastindex))
            case _:
                raise ValueError(f'Unknown pattern for {line}')
        yield tok


if __name__ == "__main__":
    with Path(__file__).parent.joinpath("input/day7_sample" if TEST_MODE else "input/day7").open() as f:
        values = [i.strip() for i in f]
        print(f'Phase 1: {phase1(values)}')
        print(f'Phase 2: {phase2(values)}')
