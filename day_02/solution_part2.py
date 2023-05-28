from typing import Tuple, List

from day_02.solution import yield_rows, decode_row, get_outcome_score, get_shape_score, Shape, Outcome, \
    outcome_scores, shape_scores, win_pairs_map

opponent_encoding = {
    'A': Shape.ROCK,
    'B': Shape.PAPER,
    'C': Shape.SCISSORS
}

player_encoding = {
    'X': Outcome.LOSS,
    'Y': Outcome.DRAW,
    'Z': Outcome.WIN
}


def find_player_shape(opponent_shape: Shape, outcome: Outcome, win_pairs_map: List[Tuple]) -> Shape:
    if outcome == Outcome.DRAW:
        return opponent_shape
    elif outcome == Outcome.WIN:
        return next(pair[1] for pair in win_pairs_map if pair[0] == opponent_shape)
    return next(pair[0] for pair in win_pairs_map if pair[1] == opponent_shape)


if __name__ == '__main__':
    path = './input.txt'

    total_score = 0
    for encoded_row in yield_rows(path):
        opponent_shape, desired_outcome = decode_row(encoded_row, opponent_encoding, player_encoding)
        player_shape = find_player_shape(opponent_shape, desired_outcome, win_pairs_map)
        round_score = get_outcome_score(opponent_shape,
                                        player_shape,
                                        outcome_scores,
                                        win_pairs_map) + get_shape_score(player_shape, shape_scores)
        total_score += round_score

    print(total_score)
