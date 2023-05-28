from __future__ import annotations

import time
from collections import namedtuple
from typing import List, Set

import numpy as np

from day_02.solution import yield_rows

Coord = namedtuple('Coord', 'x y')


def down(coord: Coord) -> Coord:
    return Coord(coord.x, coord.y + 1)


def down_left(coord: Coord) -> Coord:
    return Coord(coord.x - 1, coord.y + 1)


def down_right(coord: Coord) -> Coord:
    return Coord(coord.x + 1, coord.y + 1)


def parse_rock_path(path: str) -> Set[Coord]:
    path_coords = [Coord(int(position.split(',')[0]), int(position.split(',')[1])) for position in path.split(' -> ')]

    path_rocks = set()
    for path_start, path_end in zip(path_coords, path_coords[1:]):
        # Only one dimension should change in one path of rocks
        if path_start.x != path_end.x and path_start.y != path_end.y:
            raise ValueError('Two dimensions has changed in a path of rocks')

        for x in range(min(path_start.x, path_end.x), max(path_start.x, path_end.x) + 1):
            for y in range(min(path_start.y, path_end.y), max(path_start.y, path_end.y) + 1):
                path_rocks.add(Coord(x, y))

    return path_rocks


class Cave:
    def __init__(self, rock_positions: Set[Coord], sand_positions: Set[Coord],
                 sand_start_point: Coord = Coord(500, 0)) -> None:
        self.rock_positions = rock_positions
        self.sand_positions = sand_positions
        self.sand_start_point = sand_start_point

        self.bottom_rock_pos = max(p.y for p in rock_positions)

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
        if not self.is_empty(self.sand_start_point):
            raise RuntimeError('There is no place for another sand unit.')

        return Coord(self.sand_start_point.x, self.sand_start_point.y)

    def simulate_sand_unit(self) -> bool:
        sand_pos = self.produce_sand()

        while True:
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
            if self.is_empty(down(sand_pos)):
                sand_pos = down(sand_pos)
            elif self.is_empty(down_left(sand_pos)):
                sand_pos = down_left(sand_pos)
            elif self.is_empty(down_right(sand_pos)):
                sand_pos = down_right(sand_pos)
            else:
                # Unit of sand comes to rest
                self.sand_positions.add(sand_pos)
                return True


def visualise_cave(cave: Cave) -> np.ndarray:
    all_objects = cave.sand_positions.union(cave.rock_positions).union([cave.sand_start_point])
    min_x = min(p.x for p in all_objects)
    max_x = max(p.x for p in all_objects)
    min_y = min(p.y for p in all_objects)
    max_y = max(p.y for p in all_objects)

    range_x = max_x - min_x + 1
    range_y = max_y - min_y + 1

    print(min_x, min_y, max_x, max_y)
    print(range_x, range_y)

    cave_layout = np.full((range_y, range_x), ' ')

    for s in cave.sand_positions:
        cave_layout[s.y - min_y, s.x - min_x] = 'o'
    for r in cave.rock_positions:
        cave_layout[r.y - min_y, r.x - min_x] = '#'

    cave_layout[cave.sand_start_point.y - min_y, cave.sand_start_point.x - min_x] = '+'

    return cave_layout


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
