from pathlib import Path
import sys
import math

TEST_MODE = bool(len(sys.argv) > 1 and sys.argv[1] == "test")


def phase1(v):
    packet, index = read_packet(0, v)
    return packet.sum_of_versions()


def phase2(v):
    packet, index = read_packet(0, v)
    return packet.calc()


def read_packet(index, v):
    version, packet_type, index = read_header(v, index)

    sub_packets = []
    literal = ''

    if packet_type != 4:

        length_type, length, index = read_length(v, index)

        if length_type == 1:
            for i in range(length):
                packet, index = read_packet(index, v)
                sub_packets.append(packet)
        else:
            while length > 0:
                start = index
                packet, index = read_packet(index, v)
                sub_packets.append(packet)
                length -= index - start
    else:
        last = False
        temp = ''
        while not last:
            last, value, index = read_literal(v, index)
            temp += value
        literal = to_number(temp)

    return Packet(version, sub_packets, literal, packet_type), index


class Packet:
    def __init__(self, version, sub_packets, literal, type):
        self.version = version
        self.literal = literal
        self.sub_packets = sub_packets
        self.type = type

    def sum_of_versions(self):
        return self.version + sum([s.sum_of_versions() for s in self.sub_packets])

    def calc(self):
        match self.type:
            case 0:
                return sum([s.calc() for s in self.sub_packets])
            case 1:
                return math.prod([s.calc() for s in self.sub_packets])
            case 2:
                return min([s.calc() for s in self.sub_packets])
            case 3:
                return max([s.calc() for s in self.sub_packets])
            case 4:
                return self.literal
            case 5:
                return 1 if self.sub_packets[0].calc() > self.sub_packets[1].calc() else 0
            case 6:
                return 1 if self.sub_packets[0].calc() < self.sub_packets[1].calc() else 0
            case 7:
                return 1 if self.sub_packets[0].calc() == self.sub_packets[1].calc() else 0

    def __repr__(self):
        return f"<version:{self.version}, packets:{self.sub_packets}, literal:{self.literal} type:{self.type}"


def to_number(binary):
    return int(binary, 2)


def read_literal(v, index):
    return True if v[index] == '0' else False, v[index + 1:index + 5], index + 5


def read_length(v, index):
    if v[index:index + 1] == '0':
        return 0, to_number(v[index + 1:index + 16]), index + 16
    else:
        return 1, to_number(v[index + 1:index + 12]), index + 12


def read_header(v, i):
    return to_number(v[i:i + 3]), to_number(v[i + 3:i + 6]), i + 6


def load(code):
    return ''.join([hex_dict[i] for i in code])


hex_dict = {
    '0': '0000',
    '1': '0001',
    '2': '0010',
    '3': '0011',
    '4': '0100',
    '5': '0101',
    '6': '0110',
    '7': '0111',
    '8': '1000',
    '9': '1001',
    'A': '1010',
    'B': '1011',
    'C': '1100',
    'D': '1101',
    'E': '1110',
    'F': '1111'
}

if __name__ == "__main__":
    with Path(__file__).parent.joinpath("input/day16_sample" if TEST_MODE else "input/day16").open() as f:
        values = [load(i.strip()) for i in f][0]
        print(f'Phase 1: {phase1(values)}')
        print(f'Phase 2: {phase2(values)}')
