from typing import NamedTuple

from day_02.solution import yield_rows


class Coord(NamedTuple):
    x: int
    y: int
    z: int

    def __add__(self, other):
        return Coord(*(a + b for a, b in zip(self, other)))

    def __repr__(self):
        return f'({self.x}, {self.y}, {self.z})'


def adjacent_positions(position: tuple[int, int, int]):
    neighbor_positions_relative = [Coord(-1, 0, 0),
                                   Coord(1, 0, 0),
                                   Coord(0, -1, 0),
                                   Coord(0, 1, 0),
                                   Coord(0, 0, -1),
                                   Coord(0, 0, 1)]

    for rel_pos in neighbor_positions_relative:
        yield position + rel_pos


def calculate_surface(lava_bits_positions: set[Coord]) -> int:
    total_surface = 0
    for lava_bit_position in lava_bits_positions:
        exposed_sides = 6
        for adjacent_position in adjacent_positions(lava_bit_position):
            if adjacent_position in lava_bits_positions:
                exposed_sides -= 1
        total_surface += exposed_sides
    return total_surface


if __name__ == '__main__':
    path = './input.txt'

    data = list(yield_rows(path))
    data = [row.split(',') for row in data]
    data = [[int(pos) for pos in row] for row in data]
    data = [Coord(*row) for row in data]

    lava_bits_positions = set(data)

    # part 1
    print(calculate_surface(lava_bits_positions))
