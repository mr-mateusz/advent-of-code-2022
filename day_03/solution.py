from collections import namedtuple
from typing import List, Tuple, Union

from day_02.solution import yield_rows


def split_list(lst: Union[List, str]) -> Tuple[List, List]:
    """If list has odd number of elements, the first sublist will be smaller."""
    half_idx = len(lst) // 2
    return lst[:half_idx], lst[half_idx:]


CharPriorityEntry = namedtuple('CharPriorityEntry', 'first_char last_char ascii_offset priority_offset')

char_priority_map = [
    CharPriorityEntry('a', 'z', 97, 1),
    CharPriorityEntry('A', 'Z', 65, 27)
]


def get_priority(char: str, priority_map: List[CharPriorityEntry]) -> int:
    if len(char) != 1:
        raise ValueError
    for entry in priority_map:
        if entry.first_char <= char <= entry.last_char:
            return ord(char) - entry.ascii_offset + entry.priority_offset
    raise ValueError


if __name__ == '__main__':
    path = './input.txt'

    sum_of_priorities = 0
    for rucksack_content in yield_rows(path):
        first_compartment, second_compartment = split_list(rucksack_content)

        items_from_both = set(first_compartment).intersection(second_compartment)
        if len(items_from_both) != 1:
            raise Exception
        item_from_both = next(x for x in items_from_both)
        sum_of_priorities += get_priority(item_from_both, char_priority_map)

    print(sum_of_priorities)
