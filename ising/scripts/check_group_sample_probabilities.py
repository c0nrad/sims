from functools import reduce
import math
from builder import ones_grid
from ising import Ising
import itertools
from ising_detailed_balance_group import calculate_group_probability, enumerate_all_changes_in_move
from ising_state_solution import neighbor_probabilities
from ising_state_vector import IsingStateVector, normalize_state
import numpy as np
from multiplicity import count_fit, count_unique_fits
from utils import ud_to_value, value_to_ud
import sympy
import pdb
from pprint import pprint
import random
import re
from ising_detailed_balance_pairs import (
    calculate_pair_probability,
    calculate_pair_probability_corners,
    enumerate_all_changes_in_pair_move,
)

N = 400


def get_state_at(model, x, y):
    check_middle_state = (
        model.at(x, y),
        model.at(x, y - 1),  # top
        model.at(x + 1, y),  # right
        model.at(x, y + 1),  # bottom
        model.at(x - 1, y),  # left
    )
    return "".join([value_to_ud(a) for a in check_middle_state])


def count_group_occurances(model, states):
    count = 0

    for x in range(model.gridSize):
        for y in range(model.gridSize):
            check_states = [
                get_state_at(model, x, y),
                get_state_at(model, x, y - 1),
                get_state_at(model, x + 1, y),
                get_state_at(model, x, y + 1),
                get_state_at(model, x - 1, y),
            ]

            if states == check_states:
                count += 1

            # print(middle_state, check_middle_state)
    return count


assert count_group_occurances(ones_grid(3), ["uuuuu", "uuuuu", "uuuuu", "uuuuu", "uuuuu"]) == 9
assert count_group_occurances(ones_grid(3), ["uuuuu", "uuuud", "uuuuu", "uuuuu", "uuuuu"]) == 0


def get_pair_enumeration_states(grid):
    states = []
    for middle in [(1, 1), (2, 1)]:
        x = middle[0]
        y = middle[1]
        state = (
            grid.at(x, y),
            grid.at(x, y - 1),  # top
            grid.at(x + 1, y),  # right
            grid.at(x, y + 1),  # bottom
            grid.at(x - 1, y),  # left
        )

        state = "".join([value_to_ud(a) for a in state])
        states.append((state))
    return states


if __name__ == "__main__":
    original_model = Ising(N, 2 / math.log(math.sqrt(2) + 1))
    original_model.loop(10000)
    movesets = enumerate_all_changes_in_move()

    moveset_index = 0

    final_probabilities = {}
    final_counts = {}

    for moveset in movesets:
        before_states, after_states = moveset

        final_probabilities = 0
        final_counts = 0
        for i in range(50):
            original_model.loop(10000)
            before = IsingStateVector(original_model)

            probability_of_move_occuring = calculate_group_probability(before, before_states)
            probability_of_move_occuring = probability_of_move_occuring[0] / probability_of_move_occuring[1]
            counts = count_group_occurances(original_model, before_states)
            final_probabilities += probability_of_move_occuring
            final_counts += counts

            print(i, moveset_index, len(movesets), counts, probability_of_move_occuring)

        print(before_states, after_states, final_probabilities / 100, final_counts / 100)

        moveset_index += 1

    exit(0)
