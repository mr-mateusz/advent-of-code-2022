from collections import namedtuple
from enum import Enum
from typing import Tuple, List

from day_02.solution import yield_rows

Position = namedtuple('Position', 'x y')


class Direction(Enum):
    L = Position(-1, 0)
    R = Position(1, 0)
    U = Position(0, 1)
    D = Position(0, -1)


def _move_head(head: Position, direction: Direction) -> Position:
    return Position(head.x + direction.value.x, head.y + direction.value.y)


def _get_step(head_coord: int, tail_coord: int) -> int:
    if head_coord > tail_coord:
        return 1
    return -1


def _move_tail(tail: Position, head: Position) -> Position:
    if head.x == tail.x and abs(head.y - tail.y) > 1:
        # horizontal
        return Position(tail.x, tail.y + _get_step(head.y, tail.y))
    elif head.y == tail.y and abs(head.x - tail.x) > 1:
        # vertical
        return Position(tail.x + _get_step(head.x, tail.x), tail.y)
    elif abs(head.x - tail.x) + abs(head.y - tail.y) > 2:
        # diagonal
        return Position(tail.x + _get_step(head.x, tail.x), tail.y + _get_step(head.y, tail.y))
    # no tail adjustment required
    return tail


def move_step(head: Position, tail: Position, direction: Direction) -> Tuple[Position, Position]:
    head = _move_head(head, direction)
    tail = _move_tail(tail, head)
    return head, tail


def move(head: Position, tail: Position, direction: Direction, steps: int) -> Tuple[List[Position], List[Position]]:
    assert steps > 0

    head_positions = []
    tail_positions = []

    for _ in range(steps):
        head, tail = move_step(head, tail, direction)
        head_positions.append(head)
        tail_positions.append(tail)

    return head_positions, tail_positions


class Rope:
    def __init__(self, length: int) -> None:
        assert length > 0
        self.elements = [Position(0, 0) for _ in range(length)]

    def move(self, direction: Direction) -> None:
        new_elements = [_move_head(self.elements[0], direction)]

        for elem in self.elements[1:]:
            new_elements.append(_move_tail(elem, new_elements[-1]))

        self.elements = new_elements


if __name__ == '__main__':
    path = './input.txt'

    head_pos = Position(0, 0)
    tail_pos = Position(0, 0)

    all_tail_positions = [tail_pos]
    for line in yield_rows(path):
        direction, steps = line.split()
        steps = int(steps)
        direction = Direction[direction]

        head_positions, tail_positions = move(head_pos, tail_pos, direction, steps)

        head_pos = head_positions[-1]
        tail_pos = tail_positions[-1]

        all_tail_positions.extend(tail_positions)

    # Part 1
    print(len(set(all_tail_positions)))

    rope_length = 10
    rope = Rope(rope_length)

    all_tail_positions = [rope.elements[-1]]
    for line in yield_rows(path):
        direction, steps = line.split()
        steps = int(steps)
        direction = Direction[direction]

        for _ in range(steps):
            rope.move(direction)
            all_tail_positions.append(rope.elements[-1])

    # Part 2
    print(len(set(all_tail_positions)))
