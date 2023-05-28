from __future__ import annotations

from collections import namedtuple
from dataclasses import dataclass
from typing import List, Optional

import numpy as np

from day_02.solution import yield_rows

Coord = namedtuple('Coord', 'x y')


def read_elevation_map(path: str) -> np.ndarray:
    return np.array([list(line) for line in yield_rows(path)])


def find_char(map_: np.ndarray, char: str) -> Coord:
    for x in range(map_.shape[0]):
        for y in range(map_.shape[1]):
            if map_[x, y] == char:
                return Coord(x, y)
    raise ValueError


def is_reachable(pos: Coord, map_: np.ndarray, current_elevation: str) -> bool:
    return 0 <= pos.x < map_.shape[0] and \
           0 <= pos.y < map_.shape[1] and \
           ord(map_[pos.x, pos.y]) - ord(current_elevation) <= 1


def draw_map(map_: np.ndarray, path: List[Coord]):
    map_ = np.array([[0 for _ in range(map_.shape[1])] for _ in range(map_.shape[0])])
    for index, coord in enumerate(path, start=1):
        map_[coord.x][coord.y] = index
    print(map_)


@dataclass
class Vertex:
    coord: Coord
    dist: int = 0

    def __eq__(self, other: Vertex) -> bool:
        return self.coord == other.coord


def find_shortest_path_len(map_: np.ndarray, start: Coord, end: Coord) -> Optional[int]:
    if start == end:
        return 0

    vertices = [Vertex(start)]

    for elem in vertices:
        pos = elem.coord
        dist = elem.dist
        directions = [Coord(pos.x - 1, pos.y), Coord(pos.x + 1, pos.y), Coord(pos.x, pos.y - 1),
                      Coord(pos.x, pos.y + 1)]

        for direction in directions:
            if is_reachable(direction, map_, map_[pos.x, pos.y]):
                if direction == end:
                    return dist + 1

                candidate = Vertex(direction, dist + 1)
                if candidate not in vertices:
                    vertices.append(candidate)

    return None


def is_reachable_reversed(pos: Coord, map_: np.ndarray, current_elevation: str) -> bool:
    return 0 <= pos.x < map_.shape[0] and \
           0 <= pos.y < map_.shape[1] and \
           ord(current_elevation) - ord(map_[pos.x, pos.y]) <= 1


def find_shortest_path_len_reversed_to_elevation(map_: np.ndarray, start: Coord, end_elevation: str) -> Optional[int]:
    if map_[start.x, start.y] == end_elevation:
        return 0

    vertices = [Vertex(start)]

    for elem in vertices:
        pos = elem.coord
        dist = elem.dist
        directions = [Coord(pos.x - 1, pos.y), Coord(pos.x + 1, pos.y), Coord(pos.x, pos.y - 1),
                      Coord(pos.x, pos.y + 1)]

        for direction in directions:
            if is_reachable_reversed(direction, map_, map_[pos.x, pos.y]):
                if map_[direction.x, direction.y] == end_elevation:
                    return dist + 1

                candidate = Vertex(direction, dist + 1)
                if candidate not in vertices:
                    vertices.append(candidate)

    return None


if __name__ == '__main__':
    path = './input.txt'

    elevation_map = read_elevation_map(path)

    start_pos = find_char(elevation_map, 'S')
    end_pos = find_char(elevation_map, 'E')

    elevation_map[start_pos.x, start_pos.y] = 'a'
    elevation_map[end_pos.x, end_pos.y] = 'z'

    shortest_path_len = find_shortest_path_len(elevation_map, start_pos, end_pos)

    # Part 1
    print(shortest_path_len)

    shortest_path_to_any_a_len = find_shortest_path_len_reversed_to_elevation(elevation_map, end_pos, 'a')

    # Part 2
    print(shortest_path_to_any_a_len)
