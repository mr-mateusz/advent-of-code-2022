from enum import Enum
from typing import Generator, Tuple, Dict, Any, List


def yield_rows(path: str) -> Generator[str, None, None]:
    is_eof = False
    with open(path, 'r') as f:
        while not is_eof:
            data = f.readline()
            if data == '':
                is_eof = True
            else:
                data = data.strip('\n')
                yield data


class Shape(Enum):
    ROCK = 1
    PAPER = 2
    SCISSORS = 3


class Outcome(Enum):
    WIN = 1
    LOSS = 2
    DRAW = 3


opponent_encoding = {
    'A': Shape.ROCK,
    'B': Shape.PAPER,
    'C': Shape.SCISSORS
}

player_encoding = {
    'X': Shape.ROCK,
    'Y': Shape.PAPER,
    'Z': Shape.SCISSORS
}

shape_scores = {Shape.ROCK: 1, Shape.PAPER: 2, Shape.SCISSORS: 3}

outcome_scores = {
    Outcome.WIN: 6,
    Outcome.LOSS: 0,
    Outcome.DRAW: 3,
}

win_pairs_map = [(Shape.ROCK, Shape.PAPER), (Shape.PAPER, Shape.SCISSORS), (Shape.SCISSORS, Shape.ROCK)]


def decode_row(row: str, first_encoding_map: Dict, second_encoding_map: Dict) -> Tuple[Any, Any]:
    first_encoding, second_encoding = row.split()
    return first_encoding_map[first_encoding], second_encoding_map[second_encoding]


def get_shape_score(shape: Shape, score_map: Dict) -> int:
    return score_map[shape]


def get_outcome_score(opponent_shape: Shape, your_shape: Shape, outcome_map: Dict, win_pairs: List[Tuple]) -> int:
    if your_shape == opponent_shape:
        return outcome_map[Outcome.DRAW]
    elif (opponent_shape, your_shape) in win_pairs:
        return outcome_map[Outcome.WIN]
    return outcome_map[Outcome.LOSS]


if __name__ == '__main__':
    path = './input.txt'

    total_score = 0
    for encoded_row in yield_rows(path):
        opponent_shape, player_shape = decode_row(encoded_row, opponent_encoding, player_encoding)
        round_score = get_outcome_score(opponent_shape,
                                        player_shape,
                                        outcome_scores,
                                        win_pairs_map) + get_shape_score(player_shape, shape_scores)
        total_score += round_score

    print(total_score)
