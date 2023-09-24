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


def adjacent_positions(position: Coord):
    neighbor_positions_relative = [Coord(-1, 0, 0),
                                   Coord(1, 0, 0),
                                   Coord(0, -1, 0),
                                   Coord(0, 1, 0),
                                   Coord(0, 0, -1),
                                   Coord(0, 0, 1)]

    for rel_pos in neighbor_positions_relative:
        yield position + rel_pos


def is_adjacent_to_water(position: Coord, water_positions: set[Coord]) -> bool:
    for adjacent_position in adjacent_positions(position):
        if adjacent_position in water_positions:
            return True
    return False


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

    # part 2 - simulation

    # min and max value for each coord ('edges' of the 3D space)
    coord_mins = [min(pos[i] for pos in lava_bits_positions) for i in range(3)]
    coord_maxs = [max(pos[i] for pos in lava_bits_positions) for i in range(3)]

    # initial water positions (just over the 'edges')
    water_positions = set(
        [Coord(coord_mins[0] - 1, y, z)
         for y in range(coord_mins[1], coord_maxs[1] + 1)
         for z in range(coord_mins[2], coord_maxs[2] + 1)] +
        [Coord(coord_maxs[0] + 1, y, z)
         for y in range(coord_mins[1], coord_maxs[1] + 1)
         for z in range(coord_mins[2], coord_maxs[2] + 1)] +
        [Coord(x, coord_mins[1] - 1, z)
         for x in range(coord_mins[0], coord_maxs[0] + 1)
         for z in range(coord_mins[2], coord_maxs[2] + 1)] +
        [Coord(x, coord_maxs[1] + 1, z)
         for x in range(coord_mins[0], coord_maxs[0] + 1)
         for z in range(coord_mins[2], coord_maxs[2] + 1)] +
        [Coord(x, y, coord_mins[2] - 1)
         for x in range(coord_mins[0], coord_maxs[0] + 1)
         for y in range(coord_mins[1], coord_maxs[1] + 1)] +
        [Coord(x, y, coord_maxs[2] + 1)
         for x in range(coord_mins[0], coord_maxs[0] + 1)
         for y in range(coord_mins[1], coord_maxs[1] + 1)]
    )

    # empty space positions (initially positions in 'space' without lava bits)
    empty_space_positions = set([Coord(x, y, z)
                                 for x in range(coord_mins[0], coord_maxs[0] + 1)
                                 for y in range(coord_mins[1], coord_maxs[1] + 1)
                                 for z in range(coord_mins[2], coord_maxs[2] + 1)
                                 if Coord(x, y, z) not in lava_bits_positions])

    # simulate water flooding the space
    water_expanded = True
    while water_expanded:
        water_expanded = False
        water_will_reach_positions = []
        for empty_space_position in empty_space_positions:
            if is_adjacent_to_water(empty_space_position, water_positions):
                water_will_reach_positions.append(empty_space_position)

        if water_will_reach_positions:
            water_expanded = True
            water_positions.update(water_will_reach_positions)
            empty_space_positions = empty_space_positions.difference(water_will_reach_positions)

    # now treat all 'not flooded' positions as lava positions
    lava_bits_positions.update(empty_space_positions)

    # and calculate surface for 'updated' lava positions
    # part 2
    print(calculate_surface(lava_bits_positions))
