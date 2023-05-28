from day_02.solution import yield_rows

if __name__ == '__main__':
    path = './input.txt'

    maximum_dir_size = 100_000

    total_filesystem_space = 70_000_000
    required_space = 30_000_000

    visited_dirs_size = []
    current_dir_tree_size = []
    for line in yield_rows(path):
        if line.startswith('$ cd'):
            dir_name = line.split()[-1]
            if dir_name == '..':
                visited_dirs_size.append(current_dir_tree_size.pop())
            else:
                current_dir_tree_size.append(0)
        first_word = line.split()[0]
        if first_word.isdigit():
            size = int(first_word)
            current_dir_tree_size = [dir_size + size for dir_size in current_dir_tree_size]

    visited_dirs_size = visited_dirs_size + current_dir_tree_size

    # Part 1
    total_size = sum([s for s in visited_dirs_size if s <= maximum_dir_size])
    print(total_size)

    # Part 2
    biggest_dir_size = max(visited_dirs_size)
    unused_space = total_filesystem_space - biggest_dir_size

    missing_space = required_space - unused_space

    best_dir_size_to_delete = biggest_dir_size
    for dir_size in visited_dirs_size:
        if missing_space <= dir_size < best_dir_size_to_delete:
            best_dir_size_to_delete = dir_size

    print(best_dir_size_to_delete)
