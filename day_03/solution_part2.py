from typing import List, Generator

from day_02.solution import yield_rows
from day_03.solution import get_priority, char_priority_map


def yield_chunks(path: str, chunk_size: int) -> Generator[List[str], None, None]:
    """Yield chunks of n rows from a given file"""
    chunk = []
    for row in yield_rows(path):
        chunk.append(row)
        if len(chunk) == chunk_size:
            yield chunk
            chunk = []

    # Last chunk could be smaller
    if chunk:
        yield chunk


if __name__ == '__main__':
    path = './input.txt'

    sum_of_priorities = 0
    for group_rucksack_content in yield_chunks(path, 3):
        if len(group_rucksack_content) != 3:
            raise ValueError
        common_items = set(group_rucksack_content[0]) \
            .intersection(group_rucksack_content[1]) \
            .intersection(group_rucksack_content[2])

        if len(common_items) != 1:
            raise Exception()
        common_item = next(x for x in common_items)
        sum_of_priorities += get_priority(common_item, char_priority_map)

    print(sum_of_priorities)
