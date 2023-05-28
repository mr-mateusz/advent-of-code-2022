from collections import namedtuple
from typing import List, Generator

TotalElfCalories = namedtuple('TotalElfCalories', 'elf calories')


def yield_elf_items_calories(path: str) -> Generator[List[int], None, None]:
    is_eof = False
    elf_calories = []
    with open(path, 'r', encoding='utf-8') as f:
        while not is_eof:
            data = f.readline()
            if data == '\n':
                if elf_calories:
                    yield elf_calories
                elf_calories = []
            elif data == '':
                is_eof = True
            else:
                data = int(data.strip('\n'))
                elf_calories.append(data)

        if elf_calories:
            yield elf_calories


if __name__ == '__main__':
    list_with_elf_calories = './input.txt'

    elf_with_max_calories = TotalElfCalories(-1, 0)
    for elf_index, elf_items_calories in enumerate(yield_elf_items_calories(list_with_elf_calories)):
        elf_calories = sum(elf_items_calories)

        if elf_calories > elf_with_max_calories.calories:
            elf_with_max_calories = TotalElfCalories(elf_index, elf_calories)

    print(elf_with_max_calories.calories)
