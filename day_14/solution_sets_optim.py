from __future__ import annotations

import time
from typing import List, Set

from day_02.solution import yield_rows
from day_14.solution_sets import Coord, parse_rock_path, down, down_left, down_right


class Cave:
    def __init__(self, rock_positions: Set[Coord], sand_positions: Set[Coord],
                 sand_start_point: Coord = Coord(500, 0)) -> None:
        self.rock_positions = rock_positions
        self.sand_positions = sand_positions
        self.sand_start_point = sand_start_point

        self.bottom_rock_pos = max(p.y for p in rock_positions)

        # Trace path of last sand unit
        self.last_sand_path = []

    @classmethod
    def from_rock_paths(cls, rock_paths: List[str]) -> Cave:
        rocks = set()

        for rock_path in rock_paths:
            parsed = parse_rock_path(rock_path)
            rocks.update(parsed)

        return cls(rocks, set())

    def is_empty(self, pos: Coord) -> bool:
        return pos not in self.rock_positions.union(self.sand_positions)

    def produce_sand(self) -> Coord:
        # Start from last position of previous sand unit which was not an ending position
        # (ending position was removed from a list, so last element is taken)
        if self.last_sand_path:
            return self.last_sand_path.pop()

        if not self.is_empty(self.sand_start_point):
            raise RuntimeError('There is no place for another sand unit.')

        return Coord(self.sand_start_point.x, self.sand_start_point.y)

    def simulate_sand_unit(self) -> bool:
        sand_pos = self.produce_sand()

        while True:
            # Trace sand unit positions
            self.last_sand_path.append(sand_pos)

            if sand_pos.y >= self.bottom_rock_pos:
                # sand will fall into the endless void
                return False
            elif self.is_empty(down(sand_pos)):
                sand_pos = down(sand_pos)
            elif self.is_empty(down_left(sand_pos)):
                sand_pos = down_left(sand_pos)
            elif self.is_empty(down_right(sand_pos)):
                sand_pos = down_right(sand_pos)
            else:
                # Unit of sand comes to rest
                self.sand_positions.add(sand_pos)

                # Remove last sand position (ending position)
                self.last_sand_path.pop()
                return True


class CaveWithFloor(Cave):

    def __init__(self, rock_positions: Set[Coord], sand_positions: Set[Coord],
                 sand_start_point: Coord = Coord(500, 0)) -> None:
        super().__init__(rock_positions, sand_positions, sand_start_point)

        self.floor = self.bottom_rock_pos + 2

    def is_empty(self, pos: Coord) -> bool:
        return super().is_empty(pos) and pos.y != self.floor

    def simulate_sand_unit(self) -> bool:
        sand_pos = self.produce_sand()

        while True:
            # Trace sand unit positions
            self.last_sand_path.append(sand_pos)

            if self.is_empty(down(sand_pos)):
                sand_pos = down(sand_pos)
            elif self.is_empty(down_left(sand_pos)):
                sand_pos = down_left(sand_pos)
            elif self.is_empty(down_right(sand_pos)):
                sand_pos = down_right(sand_pos)
            else:
                # Unit of sand comes to rest
                self.sand_positions.add(sand_pos)

                # Remove last sand position (ending position)
                self.last_sand_path.pop()

                return True


if __name__ == '__main__':
    path = './input.txt'

    rock_paths = list(yield_rows(path))

    cave = Cave.from_rock_paths(rock_paths)

    st = time.time()

    sand_added = True
    while sand_added:
        sand_added = cave.simulate_sand_unit()

    # Part 1
    print(len(cave.sand_positions))

    print(f'Duration: {time.time() - st}')

    cave = CaveWithFloor.from_rock_paths(rock_paths)

    st = time.time()

    sand_added = True
    while sand_added:
        try:
            sand_added = cave.simulate_sand_unit()
        except RuntimeError:
            sand_added = False

    # Part 2
    print(len(cave.sand_positions))

    print(f'Duration: {time.time() - st}')
