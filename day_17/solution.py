from __future__ import annotations

import itertools
from collections.abc import Sequence
from typing import List, NamedTuple

import numpy as np
from tqdm import tqdm


class Coord(NamedTuple):
    x: int
    y: int

    def move(self, x: int, y: int) -> Coord:
        return Coord(self.x + x, self.y + y)

    def move_left(self) -> Coord:
        return self.move(-1, 0)

    def move_right(self) -> Coord:
        return self.move(1, 0)

    def move_down(self) -> Coord:
        return self.move(0, -1)


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
            if not chamber.is_coord_available(coord.move_left()):
                return False
        return True

    def can_move_right(self, chamber: Chamber) -> bool:
        for coord in self.coords:
            if not chamber.is_coord_available(coord.move_right()):
                return False
        return True

    def can_move_down(self, chamber: Chamber) -> bool:
        for coord in self.coords:
            if not chamber.is_coord_available(coord.move_down()):
                return False
        return True

    def __move(self, x: int, y: int) -> None:
        self.coords = [coord.move(x, y) for coord in self.coords]

    def move_left(self) -> None:
        self.__move(-1, 0)

    def move_right(self) -> None:
        self.__move(1, 0)

    def move_down(self) -> None:
        self.__move(0, -1)


class Chamber:
    def __init__(self, width: int, bottom: int, rock_types_count: int, jet_pattern: str) -> None:
        self.width = width
        self.bottom = bottom

        self.coords_taken = set()

        self.rock_type_iter = itertools.cycle(range(rock_types_count))
        self.jet_iter = itertools.cycle(jet_pattern)

        self.height_history = [self.tower_height]

    def is_coord_available(self, coord: Coord) -> bool:
        if coord in self.coords_taken:
            return False
        if coord.x < 0:
            return False
        if coord.x >= self.width:
            return False
        if coord.y <= self.bottom:
            return False
        return True

    @property
    def tower_height(self) -> int:
        return max([coord.y for coord in self.coords_taken], default=self.bottom)

    def simulate(self, num_rocks: int) -> None:
        for _ in tqdm(range(num_rocks)):
            rock_type = next(self.rock_type_iter)
            rock = Rock.create(2, self.tower_height + 4, rock_type)
            rock_landed = False

            while not rock_landed:
                # self.print()
                # Push by jet
                jet_direction = next(self.jet_iter)

                if jet_direction == '<':
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
                    self.coords_taken.update(rock.coords)

                    self.height_history.append(self.tower_height)

    def print(self):
        arr = np.ones((self.tower_height + 1, self.width))
        for coord in self.coords_taken:
            arr[coord.y, coord.x] = 0

        arr = np.flip(arr, 0)[:-1, :]
        print(arr)


def find_pattern(seq: Sequence) -> tuple[None, None] | tuple[int, int]:
    for offset in range(len(seq) // 2):
        max_pattern_len = (len(seq) - offset) // 2
        for pattern_len in range(1, max_pattern_len):
            chunk_iter = iter(seq[offset:])
            first_chunk = list(itertools.islice(chunk_iter, pattern_len))

            # Assume that there is a cycle with given len
            all_match = True

            while chunk := list(itertools.islice(chunk_iter, pattern_len)):
                if len(chunk) != len(first_chunk):
                    # last chunk
                    break
                if chunk != first_chunk:
                    # pattern does not match
                    all_match = False
                    break

            if all_match:
                return offset, pattern_len

    return None, None


def calculate_height(rocks_to_fall: int,
                     offset_height_increase: Sequence[int],
                     cycle_height_increase: Sequence[int]) -> int:
    if rocks_to_fall <= len(offset_height_increase):
        return sum(offset_height_increase[:rocks_to_fall])

    total_height = 0
    remaining_rocks = rocks_to_fall

    total_height += sum(offset_height_increase)
    remaining_rocks -= len(offset_height_increase)

    full_cycles = remaining_rocks // len(cycle_height_increase)

    total_height += full_cycles * sum(cycle_height_increase)
    remaining_rocks -= full_cycles * len(cycle_height_increase)

    total_height += sum(cycle_height_increase[:remaining_rocks])

    return total_height


if __name__ == '__main__':
    path = './input.txt'

    # number of rocks for simulation. Pattern search will be performed on the results
    rocks_for_simulation = 10000

    with open(path, 'r', encoding='utf-8') as f:
        jet_pattern = f.read().strip()

    chamber = Chamber(7, 0, len(rock_types), jet_pattern)

    chamber.simulate(rocks_for_simulation)

    print(chamber.tower_height)

    height_history = chamber.height_history

    height_increase = []
    for _prev, _next in zip(height_history, height_history[1:]):
        height_increase.append(_next - _prev)

    offset, cycle_len = find_pattern(height_increase)

    if offset and cycle_len:
        print(f'Pattern found. {offset=}, {cycle_len=}')
    else:
        print('pattern not found')
        exit()

    # offset height
    offset_height_increase = height_increase[:offset]
    # cycle height
    cycle_height_increase = height_increase[offset: offset + cycle_len]

    # sanity check
    rocks_to_fall = rocks_for_simulation
    _height = calculate_height(rocks_to_fall, offset_height_increase, cycle_height_increase)
    print(_height)
    assert _height == chamber.tower_height

    # part 1
    rocks_to_fall = 2022
    print(calculate_height(rocks_to_fall, offset_height_increase, cycle_height_increase))

    # part 2
    rocks_to_fall = 1000000000000
    print(calculate_height(rocks_to_fall, offset_height_increase, cycle_height_increase))
