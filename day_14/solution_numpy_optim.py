from __future__ import annotations

import time
from enum import Enum
from typing import List, Set, Optional, Callable, Union, Tuple, Collection

import numpy as np

from day_02.solution import yield_rows
from day_14.solution_sets import Coord, parse_rock_path, down, down_left, down_right


class CaveBlock(Enum):
    EMPTY = '.'
    ROCK = '#'
    SAND = 'o'


def adjust_coord(coord: Coord, x_min: int, y_min: int) -> Coord:
    return Coord(coord.x - x_min, coord.y - y_min)


def find_rocks(matrix: np.ndarray) -> List[Coord]:
    rocks = []
    for y in range(matrix.shape[0]):
        for x in range(matrix.shape[1]):
            if matrix[y, x] == CaveBlock.ROCK.value:
                rocks.append(Coord(x, y))
    return rocks


def min_max_range(elements: Collection, key: Callable, padding: int = 0) -> Tuple[int, int, int]:
    _min = min(key(p) for p in elements) - padding
    _max = max(key(p) for p in elements) + padding
    _range = _max - _min + 1
    return _min, _max, _range


def find_padding(points: Set[Coord]) -> int:
    return min_max_range(points, key=lambda p: p.y, padding=0)[2]


class Cave:
    def __init__(self, matrix: np.ndarray, x_min: int, y_min: int, sand_start_point: Coord,
                 bottom_rock_pos: Optional[int] = None) -> None:
        self.matrix = matrix
        self.x_min = x_min
        self.y_min = y_min
        self.sand_start_point = sand_start_point

        self.bottom_rock_pos = bottom_rock_pos or max(p.y for p in find_rocks(matrix))

        # Trace path of last sand unit
        self.last_sand_path = []

    def adjust_coord(self, coord: Coord) -> Coord:
        return adjust_coord(coord, self.x_min, self.y_min)

    def sand_units_count(self) -> int:
        return (self.matrix == CaveBlock.SAND.value).sum()

    @classmethod
    def from_rock_paths(cls, rock_paths: List[str], sand_start_point: Coord = Coord(500, 0),
                        padding: Union[int, Callable] = 2) -> Cave:
        rocks = set()

        for rock_path in rock_paths:
            parsed = parse_rock_path(rock_path)
            rocks.update(parsed)

        _points = rocks.copy()
        _points.add(sand_start_point)

        padding = padding if isinstance(padding, int) else padding(_points)

        y_min, y_max, y_range = min_max_range(_points, key=lambda p: p.y, padding=padding)
        x_min, x_max, x_range = min_max_range(_points, key=lambda p: p.x, padding=padding)

        matrix = np.full((y_range, x_range), CaveBlock.EMPTY.value)

        for rock in rocks:
            rock = adjust_coord(rock, x_min, y_min)
            matrix[rock.y, rock.x] = CaveBlock.ROCK.value

        sand_start_point = adjust_coord(sand_start_point, x_min, y_min)

        return cls(matrix, x_min, y_min, sand_start_point)

    def is_empty(self, pos: Coord) -> bool:
        return self.matrix[pos.y, pos.x] == CaveBlock.EMPTY.value

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
                self.matrix[sand_pos.y, sand_pos.x] = CaveBlock.SAND.value

                # Remove last sand position (ending position)
                self.last_sand_path.pop()
                return True


class CaveWithFloor(Cave):

    def __init__(self, matrix: np.ndarray, x_min: int, y_min: int, sand_start_point: Coord,
                 bottom_rock_pos: Optional[int] = None) -> None:
        super().__init__(matrix, x_min, y_min, sand_start_point, bottom_rock_pos)

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
                self.matrix[sand_pos.y, sand_pos.x] = CaveBlock.SAND.value

                # Remove last sand position (ending position)
                self.last_sand_path.pop()

                return True


def visualise_cave(cave: Cave) -> np.ndarray:
    return cave.matrix.copy()


if __name__ == '__main__':
    path = './input.txt'

    rock_paths = list(yield_rows(path))

    cave = Cave.from_rock_paths(rock_paths)

    st = time.time()

    sand_added = True
    while sand_added:
        sand_added = cave.simulate_sand_unit()

    # Part 1
    print(cave.sand_units_count())

    print(f'Duration: {time.time() - st}')

    cave = CaveWithFloor.from_rock_paths(rock_paths, padding=find_padding)

    st = time.time()

    sand_added = True
    while sand_added:
        try:
            sand_added = cave.simulate_sand_unit()
        except RuntimeError:
            sand_added = False

    # Part 2
    print(cave.sand_units_count())

    print(f'Duration: {time.time() - st}')
