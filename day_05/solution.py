from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Optional, List, Dict

from day_02.solution import yield_rows


class StackElement:
    def __init__(self, value: Any, next_elem: StackElement) -> None:
        self.value = value
        self.next_elem = next_elem


class Stack:
    def __init__(self) -> None:
        self.head: Optional[StackElement] = None
        self.size: int = 0

    def push(self, value: Any) -> None:
        self.head = StackElement(value, self.head)
        self.size += 1

    def pop(self) -> Any:
        if self.head is None:
            raise IndexError('Stack is empty')
        value = self.head.value
        self.head = self.head.next_elem
        self.size -= 1
        return value

    def get(self) -> Any:
        if self.head is None:
            raise IndexError('Stack is empty')
        return self.head.value

    def get_all(self, top_first: bool = True) -> List:
        elements = []
        current = self.head
        while current:
            elements.append(current.value)
            current = current.next_elem

        if top_first:
            return elements
        return list(reversed(elements))

    def __len__(self) -> int:
        return self.size


class Instruction:
    def __init__(self, how_many: int, from_stack: int, to_stack: int) -> None:
        self.how_many = how_many  # move
        self.from_stack = from_stack  # from
        self.to_stack = to_stack  # to

    @classmethod
    def from_string(cls, instruction: str) -> Instruction:
        """
        move 3 from 4 to 3
        0    1 2    3 4  5
        """
        instruction_words = instruction.split()
        return cls(int(instruction_words[1]), int(instruction_words[3]), int(instruction_words[5]))


@dataclass
class StackInfo:
    id: int
    position: int


class Cargo:
    def __init__(self, stacks: Dict[int, Stack]) -> None:
        self.stacks = stacks

    @classmethod
    def from_drawing(cls, drawing: List[str]) -> Cargo:
        # line with stack indexes
        stack_indexes_line: str = drawing[-1]
        stack_indexes = [StackInfo(int(value), position) for position, value in enumerate(stack_indexes_line) if
                         value.isdigit()]
        stacks = {stack_index.id: Stack() for stack_index in stack_indexes}

        # Reversed - decode the drawing from bottom to top, skip last line
        for cargo_line in reversed(drawing[:-1]):
            for stack_index in stack_indexes:
                crate = cargo_line[stack_index.position]
                if crate != ' ':
                    stacks[stack_index.id].push(crate)

        return cls(stacks)

    def _take_off_the_top(self, count: int, stack_id: int) -> Stack:
        removed_crates = Stack()
        for _ in range(count):
            removed_crates.push(self.stacks[stack_id].pop())
        return removed_crates

    def _put_on_top(self, crates: Stack, stack_id: int) -> None:
        for _ in range(len(crates)):
            self.stacks[stack_id].push(crates.pop())

    def move_crates_in_batch(self, instruction: str) -> None:
        instruction = Instruction.from_string(instruction)

        crates = self._take_off_the_top(instruction.how_many, instruction.from_stack)
        self._put_on_top(crates, instruction.to_stack)

    def move_crates(self, instruction: str) -> None:
        instruction = Instruction.from_string(instruction)

        for _ in range(instruction.how_many):
            self.stacks[instruction.to_stack].push(self.stacks[instruction.from_stack].pop())

    def get_top_elements(self) -> str:
        stacks_top_elements = [(stack_id, stack.get()) for stack_id, stack in self.stacks.items()]
        stacks_top_elements = [x[1] for x in sorted(stacks_top_elements, key=lambda x: x[0])]
        return ''.join(stacks_top_elements)


class CargoPrinter:
    @staticmethod
    def print(cargo: Cargo) -> None:
        # Prepare cargo data
        stack_indexes = [StackInfo(stack_id, 1 + (stack_id - 1) * 4) for stack_id in sorted(cargo.stacks.keys())]
        stacks_data = {stack_id: stack.get_all(top_first=False) for stack_id, stack in cargo.stacks.items()}

        # Calculate img size
        img_width = len(stack_indexes) * 4 - 1
        img_height = max([len(s) for s in stacks_data.values()]) + 1

        # Create img template
        img = [[' ' for _ in range(img_width)] for _ in range(img_height)]

        # Stack indexes - last row
        for si in stack_indexes:
            img[0][si.position] = str(si.id)

        for layer_index, layer in enumerate(img[1:]):
            for si in stack_indexes:
                try:
                    crate = stacks_data[si.id][layer_index]
                    layer[si.position] = crate
                    layer[si.position - 1] = '['
                    layer[si.position + 1] = ']'
                except IndexError:
                    pass

        for i in reversed(img):
            print(''.join(i))


if __name__ == '__main__':
    path = './input.txt'

    task_part = 1  # 1/2

    initial_cargo_drawing = []
    drawing_found = False
    for line in yield_rows(path):
        if line != '' and not drawing_found:
            # Drawing line
            initial_cargo_drawing.append(line)
        elif line == '' and not drawing_found:
            # Empty line between drawing lines and instruction lines
            drawing_found = True
            cargo = Cargo.from_drawing(initial_cargo_drawing)
            # CargoPrinter.print(cargo)
        else:
            # Instruction line
            # Move cargo according to the instruction
            if not drawing_found:
                raise Exception('Bad input file format. First instruction line found, but drawing was not found yet.')

            if task_part == 1:
                cargo.move_crates(line)
            else:
                cargo.move_crates_in_batch(line)
            # print(line)
            # CargoPrinter.print(cargo)

    print(cargo.get_top_elements())
