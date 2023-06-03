from __future__ import annotations

import itertools
from dataclasses import dataclass
from typing import List

import numpy as np


# Todo - make coord immutable
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
        for coord in self.coords:
            if not chamber.is_coord_available(Coord(coord.x - 1, coord.y)):
                return False
        return True

    def can_move_right(self, chamber: Chamber) -> bool:
        for coord in self.coords:
            if not chamber.is_coord_available(Coord(coord.x + 1, coord.y)):
                return False
        return True

    def can_move_down(self, chamber: Chamber) -> bool:
        for coord in self.coords:
            if not chamber.is_coord_available(Coord(coord.x, coord.y - 1)):
                return False
        return True

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

        # todo change Coord from dataclass to namedtuple and change the list below to set
        self.coords_taken = []

        self.rock_type_iter = itertools.cycle(range(rock_types_count))
        self.jet_iter = itertools.cycle(jet_pattern)

    def is_coord_available(self, coord: Coord) -> bool:
        if coord in self.coords_taken:
            return False
        if coord.x < 0:
            return False
        if coord.x > self.width:
            return False
        if coord.y <= self.bottom:
            return False
        return True

    @property
    def tower_height(self) -> int:
        return max([coord.y for coord in self.coords_taken], default=self.bottom)

    def simulate(self, num_rocks: int) -> None:
        # todo
        for _ in range(num_rocks):
            rock_type = next(self.rock_type_iter)
            rock = Rock.create(2, self.tower_height + 4, rock_type)
            rock_landed = False

            while not rock_landed:
                self.print()
                # Push by jet
                jet_direction = next(self.jet_iter)

                if jet_direction == '<':  # todo - enum
                    if rock.can_move_left(self):
                        rock.move_left()
                elif jet_direction == '>':
                    if rock.can_move_right(self):
                        rock.move_right()

                # Fall down
                if rock.can_move_down(self):
                    rock.move_down()
                else:
                    rock_landed = True
                    self.coords_taken.extend(rock.coords)

    def print(self):
        # fixme
        arr = np.ones((self.tower_height + 1, self.width))
        for coord in self.coords_taken:
            arr[coord.y, coord.x] = 0

        arr = np.flip(arr, 0)[:-1, :]
        print(arr)



if __name__ == '__main__':
    path = './input2.txt'

    rocks_to_fall = 2

    with open(path, 'r', encoding='utf-8') as f:
        jet_pattern = f.read().strip()

    chamber = Chamber(7, 0, len(rock_types), jet_pattern)

    chamber.simulate(rocks_to_fall)

    print(max([coord.y for coord in chamber.coords_taken]))

    print(chamber.coords_taken)

    chamber.print()
