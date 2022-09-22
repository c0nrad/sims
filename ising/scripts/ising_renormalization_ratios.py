from builder import (
    generate_board_from_vector_probabilistic,
    generate_board_from_vector_probabilistic_fitted,
    generate_board_from_vector_probabilistic_sprinkle,
)
from ising import Ising
from ising_state_vector import IsingStateVector
from math import sqrt


def do_small_block(board, original_n):
    blocked = Ising(N / 2, 1)

    for x in range(0, original_n, 2):
        for y in range(0, original_n, 2):
            block = board.at(x, y) + board.at(x + 1, y) + board.at(x, y + 1) + board.at(x + 1, y + 1)
            if block > 0:
                blocked.set(x // 2, y // 2, 1)
            elif block < 0:
                blocked.set(x // 2, y // 2, -1)
            else:
                blocked.set(x // 2, y // 2, board.at(x, y))

    blocked.dump()
    return blocked


if __name__ == "__main__":
    original_vector = IsingStateVector(None)
    original_vector.states = {
        "uuuuu": 1 / 8,
        "uuuud": 1 / sqrt(2) - 1 / 2,
        "uuudd": 3 / 2 - sqrt(2),
        "uudud": 3 / 4 - 1 / sqrt(2),
        "uuddd": 5 / sqrt(2) - 7 / 2,
        "udddd": 17 / 8 - 3 / sqrt(2),
        "ddddd": 1 / 8,
        "ddddu": 1 / sqrt(2) - 1 / 2,
        "ddduu": 3 / 2 - sqrt(2),
        "ddudu": 3 / 4 - 1 / sqrt(2),
        "dduuu": 5 / sqrt(2) - 7 / 2,
        "duuuu": 17 / 8 - 3 / sqrt(2),
    }

    # original_vector.states = {
    #     "uuuuu": 1 / 8 + 0.2 + 0.1 + 0.1 + 0.05,
    #     "uuuud": 1 / sqrt(2) - 1 / 2 - 0.1 - 0.1,
    #     "uuudd": 3 / 2 - sqrt(2) - 0.05,
    #     "uudud": 3 / 4 - 1 / sqrt(2),
    #     "uuddd": 5 / sqrt(2) - 7 / 2,
    #     "udddd": 17 / 8 - 3 / sqrt(2),
    #     "ddddd": 1 / 8 - 0.1,
    #     "ddddu": 1 / sqrt(2) - 1 / 2 - 0.1 - 0.1,
    #     "ddduu": 3 / 2 - sqrt(2),
    #     "ddudu": 3 / 4 - 1 / sqrt(2),
    #     "dduuu": 5 / sqrt(2) - 7 / 2,
    #     "duuuu": 17 / 8 - 3 / sqrt(2) + 0.1,
    # }
    N = 20

    assert abs(sum(original_vector.states.values()) - 1) < 0.0001, sum(original_vector.states.values()) - 1
    board = generate_board_from_vector_probabilistic_fitted(original_vector, N)
    board.dump()

    verify_vector = IsingStateVector(board)
    for state in verify_vector.states:
        print(state, original_vector.states[state], "->", verify_vector.states[state] / (N) ** 2)
    assert sum(verify_vector.states.values()) / (N) ** 2 == 1

    exit(1)
    board_blocked = do_small_block(board, N)
    final_vector = IsingStateVector(board_blocked)

    assert sum(final_vector.states.values()) / (N / 2) ** 2 == 1

    for state in final_vector.states:
        print(state, original_vector.states[state], "->", final_vector.states[state] / (N / 2) ** 2)
