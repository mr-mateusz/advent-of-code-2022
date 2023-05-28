from enum import Enum

from day_02.solution import yield_rows


class Command(Enum):
    NOOP = 'noop'
    ADDX = 'addx'


if __name__ == '__main__':
    path = './input.txt'

    reg_x = 1
    cycle = 0

    reg_x_history = [reg_x]

    for line in yield_rows(path):
        command = Command(line.split()[0])

        if command == Command.NOOP:
            cycle += 1
            reg_x_history.append(reg_x)
        elif command == Command.ADDX:
            value = int(line.split()[1])
            for _ in range(1):
                cycle += 1
                reg_x_history.append(reg_x)
            reg_x += value
            cycle += 1
            reg_x_history.append(reg_x)

    signal_strength = 0
    for i in range(1, len(reg_x_history) + 1):
        if (i - 20) % 40 == 0:
            cycle_signal_strength = reg_x_history[i - 1] * i
            signal_strength += cycle_signal_strength
            print(i, cycle_signal_strength)

    # Part 1
    print(signal_strength)

    crt = []
    crt_row = []

    reg_x = 1
    cycle = 0

    for line in yield_rows(path):
        command = Command(line.split()[0])

        if command == Command.NOOP:
            if abs((cycle % 40) - reg_x) <= 1:
                crt_row.append('#')
            else:
                crt_row.append('.')
            if len(crt_row) == 40:
                crt.append(crt_row)
                crt_row = []

            cycle += 1

        elif command == Command.ADDX:
            value = int(line.split()[1])
            for _ in range(1):
                if abs((cycle % 40) - reg_x) <= 1:
                    crt_row.append('#')
                else:
                    crt_row.append('.')
                if len(crt_row) == 40:
                    crt.append(crt_row)
                    crt_row = []

                cycle += 1

            if abs((cycle % 40) - reg_x) <= 1:
                crt_row.append('#')
            else:
                crt_row.append('.')
            if len(crt_row) == 40:
                crt.append(crt_row)
                crt_row = []

            reg_x += value
            cycle += 1

    # Part 2
    for row in crt:
        print(''.join(row))
