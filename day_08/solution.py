import numpy as np


def load_array(path: str) -> np.ndarray:
    with open(path, 'r') as f:
        data = f.readlines()

    data = [[int(value) for value in line.strip()] for line in data]
    return np.array(data)


def __check_visibility(line: np.ndarray) -> np.ndarray:
    current_highest = -1

    results = []
    for value in line:
        if value > current_highest:
            results.append(1)
            current_highest = value
        else:
            results.append(0)
    return np.array(results)


def __check_visibility_from_left(height_map: np.ndarray, visibility_map: np.ndarray, row_idx: int) -> None:
    res = __check_visibility(height_map[row_idx, :])

    for col_idx, value in enumerate(res):
        if value:
            visibility_map[row_idx, col_idx] = 1


def __check_visibility_from_right(height_map: np.ndarray, visibility_map: np.ndarray, row_idx: int) -> None:
    res = __check_visibility(np.flip(height_map[row_idx, :], 0))

    for col_idx, value in enumerate(np.flip(res, 0)):
        if value:
            visibility_map[row_idx, col_idx] = 1


def __check_visibility_from_top(height_map: np.ndarray, visibility_map: np.ndarray, col_idx: int) -> None:
    res = __check_visibility(height_map[:, col_idx])

    for row_idx, value in enumerate(res):
        if value:
            visibility_map[row_idx, col_idx] = 1


def __check_visibility_from_bottom(height_map: np.ndarray, visibility_map: np.ndarray, col_idx: int) -> None:
    res = __check_visibility(np.flip(height_map[:, col_idx], 0))

    for row_idx, value in enumerate(np.flip(res, 0)):
        if value:
            visibility_map[row_idx, col_idx] = 1


def create_tree_visibility_map(height_map: np.ndarray) -> np.ndarray:
    n_rows, n_cols = height_map.shape
    visibility_map = np.zeros((n_rows, n_cols))

    for row_idx in range(n_rows):
        __check_visibility_from_left(height_map, visibility_map, row_idx)
        __check_visibility_from_right(height_map, visibility_map, row_idx)

    for col_idx in range(n_cols):
        __check_visibility_from_top(height_map, visibility_map, col_idx)
        __check_visibility_from_bottom(height_map, visibility_map, col_idx)

    return visibility_map


def __find_visibility_distance(line: np.ndarray, current_height: int) -> int:
    for index, value in enumerate(line, start=1):
        if value >= current_height:
            return index
    return len(line)


def __view_left(height_map: np.ndarray, row_idx: int, col_idx: int) -> np.ndarray:
    return np.flip(height_map[row_idx, :col_idx])


def __view_right(height_map: np.ndarray, row_idx: int, col_idx: int) -> np.ndarray:
    return height_map[row_idx, col_idx + 1:]


def __view_up(height_map: np.ndarray, row_idx: int, col_idx: int) -> np.ndarray:
    return np.flip(height_map[:row_idx, col_idx])


def __view_down(height_map: np.ndarray, row_idx: int, col_idx: int) -> np.ndarray:
    return height_map[row_idx + 1:, col_idx]


def calculate_scenic_scores(height_map: np.ndarray) -> np.ndarray:
    n_rows, n_cols = height_map.shape
    scenic_scores = np.zeros((n_rows, n_cols))

    for row_idx in range(n_rows):
        for col_idx in range(n_cols):
            current_height = height_map[row_idx, col_idx]
            left_dist = __find_visibility_distance(__view_left(height_map, row_idx, col_idx), current_height)
            right_dist = __find_visibility_distance(__view_right(height_map, row_idx, col_idx), current_height)
            up_dist = __find_visibility_distance(__view_up(height_map, row_idx, col_idx), current_height)
            down_dist = __find_visibility_distance(__view_down(height_map, row_idx, col_idx), current_height)
            score = left_dist * right_dist * up_dist * down_dist
            scenic_scores[row_idx, col_idx] = score

    return scenic_scores


if __name__ == '__main__':
    path = './input.txt'

    tree_height_map = load_array(path)

    # Part 1
    visible_trees = create_tree_visibility_map(tree_height_map)

    print(int(visible_trees.sum()))

    # Part 2
    scenic_scores = calculate_scenic_scores(tree_height_map)

    print(int(scenic_scores.max()))
