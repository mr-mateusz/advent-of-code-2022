from typing import Generator


def yield_chars(path: str) -> Generator[str, None, None]:
    is_eof = False
    with open(path, 'r', encoding='utf-8') as f:
        while not is_eof:
            character = f.read(1)
            if not character:
                is_eof = True
            else:
                yield character


if __name__ == '__main__':
    path = './input.txt'

    distinct_chars_required = 14  # part1 - 4 / part2 - 14

    last_chars = []
    for index, character in enumerate(yield_chars(path)):
        if len(last_chars) < distinct_chars_required:
            last_chars.append(character)
        else:
            last_chars.append(character)
            last_chars.pop(0)

        if len(set(last_chars)) == distinct_chars_required:
            print(index + 1)
            break
