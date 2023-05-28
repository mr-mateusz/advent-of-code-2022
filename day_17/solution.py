from __future__ import annotations

import itertools
from dataclasses import dataclass
from typing import List


@dataclass
class Coord:
    x: int
    y: int


rock_types = [
    [(0, 0), (1, 0), (2, 0), (3, 0)],
    [(0, 1), (1, 0), (1, 1), (1, 2), (2, 1)],
    [(0, 0), (1, 0), (2, 0), (2, 1), (2, 2)],
    [(0, 0), (0, 1), (0, 2), (0, 3)],
    [(0, 0), (0, 1), (1, 0), (1, 1)]
]


def generate_rock_coords(left: int, bottom: int, rock_type: int) -> List[Coord]:
    try:
        return [Coord(c[0] + left, c[1] + bottom) for c in rock_types[rock_type]]
    except IndexError:
        raise ValueError(f'Incorrect {rock_type=}')


class Rock:
    def __init__(self, coords: List[Coord]):
        self.coords = coords

    @classmethod
    def create(cls, left: int, bottom: int, rock_type: int) -> Rock:
        return cls(generate_rock_coords(left, bottom, rock_type))

    def can_move_left(self, chamber: Chamber) -> bool:
        pass

    def can_move_right(self, chamber: Chamber) -> bool:
        pass

    def can_move_down(self, chamber: Chamber) -> bool:
        pass

    def __move(self, x: int, y: int) -> None:
        for coord in self.coords:
            coord.x += x
            coord.y += y

    def move_left(self) -> None:
        self.__move(-1, 0)

    def move_right(self) -> None:
        self.__move(1, 0)

    def move_down(self) -> None:
        self.__move(0, -1)


class Chamber:

    # todo - rock types instead of count
    def __init__(self, width: int, bottom: int, rock_types_count: int, jet_pattern: str) -> None:
        self.width = width
        self.bottom = bottom

        self.coords_taken = []

        self.rock_type_iter = itertools.cycle(range(rock_types_count))
        self.jet_iter = itertools.cycle(jet_pattern)


if __name__ == '__main__':
    path = './input2.txt'
    path = 'year_2022/day_17/input2.txt'

    with open(path, 'r', encoding='utf-8') as f:
        jet_pattern = f.read().strip()
