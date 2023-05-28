from day_01.solution import yield_elf_items_calories, TotalElfCalories

if __name__ == '__main__':
    list_with_elf_calories = './input.txt'

    top_elf_calories = [TotalElfCalories(-1, 0)] * 3

    for elf_index, elf_items_calories in enumerate(yield_elf_items_calories(list_with_elf_calories)):
        elf_calories = sum(elf_items_calories)

        if elf_calories > top_elf_calories[-1].calories:
            top_elf_calories = sorted(top_elf_calories + [TotalElfCalories(elf_index, elf_calories)],
                                      key=lambda x: x.calories, reverse=True)[:3]

    print(sum(ec.calories for ec in top_elf_calories))
