from __future__ import annotations

from typing import List, Callable, Optional

from tqdm import tqdm

from day_02.solution import yield_rows


def _last_word(text: str) -> str:
    return text.strip().split()[-1]


def reduce_worry_level(value: int, by: int = 3) -> int:
    return value // by


def identity(value: int) -> int:
    return value


class Monkey:
    def __init__(self, index: int, items: List[int], operation: str, test_divisor: int,
                 monkey_when_test_true: int, monkey_when_test_false: int,
                 reduce_worry_level_func: Optional[Callable]) -> None:
        assert test_divisor != 0

        self.index = index
        self.items = items
        self.operation = operation
        self.test_divisor = test_divisor
        self.monkey_when_test_true = monkey_when_test_true
        self.monkey_when_test_false = monkey_when_test_false

        self.inspection_cnt = 0
        self.monkeys: List[Monkey] = []

        self.reduce_worry_level = reduce_worry_level_func or identity

    @classmethod
    def from_description(cls, description: List[str],
                         reduce_worry_level_func: Optional[Callable] = None) -> Monkey:
        index = int(description[0].replace('Monkey ', '').replace(':', ''))
        items = [int(item) for item in description[1].strip().replace('Starting items: ', '').split(', ')]
        operation = description[2].strip().replace('Operation: new = ', '')
        test_divisor = int(_last_word(description[3]))
        monkey_when_test_true = int(_last_word(description[4]))
        monkey_when_test_false = int(_last_word(description[5]))

        return cls(index, items, operation,
                   test_divisor, monkey_when_test_true, monkey_when_test_false, reduce_worry_level_func)

    def inspect(self, item: int) -> int:
        operation = self.operation.replace('old', str(item))
        new = eval(operation)
        self.inspection_cnt += 1
        return new

    def choose_monkey_to_throw_at(self, item: int) -> int:
        if item % self.test_divisor == 0:
            return self.monkey_when_test_true
        return self.monkey_when_test_false

    def catch(self, item: int) -> None:
        self.items.append(item)

    def throw(self, item: int, monkey_index: int) -> None:
        self.monkeys[monkey_index].catch(item)

    def turn(self):
        if not self.monkeys:
            raise ValueError('Other monkeys not set')
        for _ in range(len(self.items)):
            item = self.inspect(self.items.pop(0))
            item = self.reduce_worry_level(item)

            self.throw(item, self.choose_monkey_to_throw_at(item))


if __name__ == '__main__':
    path = './input.txt'

    n_rounds = 20
    most_active_to_count = 2

    monkeys = []

    monkey_description = []
    for line in yield_rows(path):
        if not line:
            monkeys.append(Monkey.from_description(monkey_description, reduce_worry_level))
            monkey_description = []
        else:
            monkey_description.append(line)

    if monkey_description:
        monkeys.append(Monkey.from_description(monkey_description, reduce_worry_level))

    for monkey in monkeys:
        monkey.monkeys = monkeys

    for _ in range(n_rounds):
        for monkey in monkeys:
            monkey.turn()

    monkey_business = 1
    for value in sorted([monkey.inspection_cnt for monkey in monkeys], reverse=True)[:most_active_to_count]:
        monkey_business *= value

    # Part 1
    print(monkey_business)

    n_rounds = 10000
    most_active_to_count = 2

    monkeys = []

    monkey_description = []
    for line in yield_rows(path):
        if not line:
            monkeys.append(Monkey.from_description(monkey_description))
            monkey_description = []
        else:
            monkey_description.append(line)

    if monkey_description:
        monkeys.append(Monkey.from_description(monkey_description))

    mod_reduce = 1
    for monkey in monkeys:
        mod_reduce *= monkey.test_divisor

    for monkey in monkeys:
        monkey.monkeys = monkeys
        monkey.reduce_worry_level = lambda x: x % mod_reduce

    for _ in tqdm(range(n_rounds)):
        for monkey in monkeys:
            monkey.turn()

    monkey_business = 1
    for value in sorted([monkey.inspection_cnt for monkey in monkeys], reverse=True)[:most_active_to_count]:
        monkey_business *= value

    # Part 2
    print(monkey_business)
