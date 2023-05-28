import functools
import json
from typing import List, Generator, Union

from day_02.solution import yield_rows


def yield_pairs(path: str) -> Generator[List[List[Union[List, int]]], None, None]:
    pair = []
    for line in yield_rows(path):
        if not line:
            yield pair
            pair = []
        else:
            pair.append(json.loads(line))

    if pair:
        yield pair


def is_in_order(left: List, right: List) -> bool:
    # Range instead of zip, because we want to easily check which list will run out of elements first
    for index in range(max(len(left), len(right))):
        # Get left and right values
        try:
            # Try to get left value
            left_val = left[index]
        except IndexError:
            # Left list is shorter
            return True
        try:
            # Try to get right value
            right_val = right[index]
        except IndexError:
            # Right list is shorter
            return False

        # Compare left and right values
        if isinstance(left_val, int) and isinstance(right_val, int):
            # Both values are integers
            if left_val < right_val:
                return True
            if left_val > right_val:
                return False
            # left_val == right val: move to the next element
        else:
            # At least one value is not an integer

            # Convert integer (if present) to list with one element
            left_val = [left_val] if isinstance(left_val, int) else left_val
            right_val = [right_val] if isinstance(right_val, int) else right_val

            try:
                # Compare lists
                return is_in_order(left_val, right_val)
            except ValueError:
                # Nested list comparison did not determine if the order is correct
                # Move to the next element
                pass

    # Cannot determine order
    raise ValueError('Cannot determine order')


def comparison_wrapper(left: List, right: List) -> int:
    return -1 if is_in_order(left, right) else 1


if __name__ == '__main__':
    path = './input.txt'

    correct_indices_sum = 0
    for index, pair in enumerate(yield_pairs(path), start=1):
        if is_in_order(pair[0], pair[1]):
            correct_indices_sum += index

    # Part 1
    print(correct_indices_sum)

    packets = [packet for pair in yield_pairs(path) for packet in pair]
    divider_packets = [[[2]], [[6]]]

    packets = packets + divider_packets

    decoder_key = 1
    for index, packet in enumerate(sorted(packets, key=functools.cmp_to_key(comparison_wrapper)), start=1):
        if packet in divider_packets:
            decoder_key *= index

    # Part 2
    print(decoder_key)
