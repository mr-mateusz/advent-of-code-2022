from __future__ import annotations

import math
import re
import time
from typing import Tuple, List, Optional

from day_02.solution import yield_rows


def manhattan_distance(p1: Tuple[int, ...], p2: Tuple[int, ...]) -> int:
    if len(p1) != len(p2):
        raise ValueError('Vector dimensions does not match')

    dist = 0
    for a, b in zip(p1, p2):
        dist += abs(a - b)
    return dist


def parse_log(line: str) -> Tuple[Tuple[int, int], Tuple[int, int]]:
    numbers = [int(val.strip('=')) for val in re.findall('=-?\\d+', line)]

    return (numbers[0], numbers[1]), (numbers[2], numbers[3])


class Sensor:

    def __init__(self, position: Tuple[int, int], closest_beacon_dist: int) -> None:
        self.position = position
        self.closest_beacon_dist = closest_beacon_dist

    @classmethod
    def from_closest_beacon(cls, sensor_pos: Tuple[int, int], beacon_pos: Tuple[int, int]) -> Sensor:
        dist = manhattan_distance(sensor_pos, beacon_pos)
        return cls(sensor_pos, dist)

    def has_in_range(self, pos: Tuple[int, int]) -> bool:
        return manhattan_distance(self.position, pos) <= self.closest_beacon_dist

    def find_forbidden_positions_along_y(self, y: int) -> List[Tuple[int, int]]:
        y_dist = abs(y - self.position[1])

        if y_dist > self.closest_beacon_dist:
            return []

        diff = self.closest_beacon_dist - y_dist

        positions = []
        for x in range(self.position[0] - diff, self.position[0] + diff + 1):
            positions.append((x, y))

        return positions


class Line:
    def __init__(self, value: int, slope: int):
        if slope not in [1, -1]:
            raise ValueError('Incorrect slope value.')

        self.value = value
        self.slope = slope

    @classmethod
    def between(cls, line1: Line, line2: Line) -> Line:
        if line1.slope != line2.slope:
            raise ValueError('Slopes does not match')

        return cls(math.floor((line1.value + line2.value) / 2), line1.slope)

    def dist(self, other: Line) -> int:
        return abs(self.value - other.value)

    def intersection(self, other: Line) -> Optional[Tuple]:
        if self.slope + other.slope != 0:
            # Parallel lines
            return None

        x = int((self.value + other.value) / 2)
        y = x - min(self.value, other.value)

        return x, y

    def __repr__(self):
        return f'{self.__class__.__name__}({self.value=}, {self.slope=})'

    def __eq__(self, other: Line):
        if not isinstance(other, Line):
            raise ValueError()
        return self.value == other.value and self.slope == other.slope

    def __hash__(self):
        return hash((self.value, self.slope))


class SensorArea:
    """
                   . top point
    start line b  /#\ end line a
                 /###\
                .##S##.
                 \###/
    start line a  \#/ end line b
                   . bottom point

    """

    def __init__(self, sensor: Sensor):
        self.sensor = sensor

        rect_top = self.find_top_point(sensor)
        rect_bot = self.find_bot_point(sensor)

        self.start_line_a = Line(rect_bot[0] - rect_bot[1], 1)
        self.end_line_a = Line(rect_top[0] - rect_top[1], 1)
        self.start_line_b = Line(rect_top[0] + rect_top[1], - 1)
        self.end_line_b = Line(rect_bot[0] + rect_bot[1], -1)

    @staticmethod
    def find_top_point(sensor: Sensor) -> Tuple:
        return sensor.position[0], sensor.position[1] - sensor.closest_beacon_dist

    @staticmethod
    def find_bot_point(sensor: Sensor) -> Tuple:
        return sensor.position[0], sensor.position[1] + sensor.closest_beacon_dist


def is_in_range(location: Tuple[int, int], sensors: List[Sensor]) -> bool:
    for sensor in sensors:
        if sensor.has_in_range(location):
            return True
    return False


def calculate_tuning_frequency(location: Tuple[int, int]) -> int:
    return location[0] * 4000000 + location[1]


if __name__ == '__main__':
    path = './input.txt'

    sensor_logs = list(yield_rows(path))

    # [(sensor_pos, beacon_pos), ...]
    sensor_data = [parse_log(line) for line in sensor_logs]

    sensors = [Sensor.from_closest_beacon(*d) for d in sensor_data]

    y_to_check = 2000000

    st = time.perf_counter()
    forbidden_positions = set()
    for sensor in sensors:
        forbidden_positions.update(sensor.find_forbidden_positions_along_y(y_to_check))

    forbidden_positions.difference_update([s[1] for s in sensor_data])

    # Part 1
    print(len(forbidden_positions))
    print(f'time: {time.perf_counter() - st}')

    st = time.perf_counter()
    sensor_areas = [SensorArea(sensor) for sensor in sensors]

    lines_a = set()
    lines_b = set()
    for area in sensor_areas:
        for other_area in sensor_areas:
            if area.start_line_a.dist(other_area.end_line_a) == 2:
                lines_a.add(Line.between(area.start_line_a, other_area.end_line_a))
            if area.start_line_b.dist(other_area.end_line_b) == 2:
                lines_b.add(Line.between(area.start_line_b, other_area.end_line_b))

    possible_locations = []
    for line_a in lines_a:
        for line_b in lines_b:
            possible_locations.append(line_a.intersection(line_b))

    # Part 2
    for location in possible_locations:
        if not is_in_range(location, sensors):
            print(calculate_tuning_frequency(location))
            break

    print(f'time: {time.perf_counter() - st}')
