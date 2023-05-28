from __future__ import annotations

from typing import Tuple

from day_02.solution import yield_rows


class Assignment:
    def __init__(self, start: int, end: int) -> None:
        self.start = start
        self.end = end

    @classmethod
    def from_range(cls, assignment_range: str) -> Assignment:
        """

        :param assignment_range: 'start-end' e.g. '1-2'; '4-6'
        :return:
        """
        split = assignment_range.split('-')
        if len(split) != 2:
            raise ValueError('Incorrect range')
        start, end = split
        return cls(int(start), int(end))

    def __contains__(self, item: Assignment) -> bool:
        if not isinstance(item, Assignment):
            raise ValueError
        return self.start <= item.start and item.end <= self.end

    def overlap(self, item: Assignment) -> bool:
        return not (item.start < self.start and item.end < self.start or item.start > self.end and item.end > self.end)


def decode_row(line: str) -> Tuple[Assignment, Assignment]:
    assignment_pair = line.split(',')
    if len(assignment_pair) != 2:
        raise ValueError('Incorrect line')
    a1, a2 = assignment_pair
    return Assignment.from_range(a1), Assignment.from_range(a2)


if __name__ == '__main__':
    path = './input.txt'

    assignments_covered = 0
    assignments_overlapped = 0
    for line in yield_rows(path):
        assignment1, assignment2 = decode_row(line)
        if assignment1 in assignment2 or assignment2 in assignment1:
            assignments_covered += 1
        if assignment1.overlap(assignment2):
            assignments_overlapped += 1

    print(assignments_covered)
    print(assignments_overlapped)
