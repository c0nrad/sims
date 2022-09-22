from functools import reduce
import math
from builder import ones_grid
from ising import Ising
import itertools
from ising_detailed_balance_group import to_mathematica
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
from math import sqrt


if __name__ == "__main__":
    before = IsingStateVector(None)
    before.states = {
        "uuuuu": sympy.symbols('a', real=True, positive=True, nonzero=True),
        "uuuud": sympy.symbols('b', real=True, positive=True, nonzero=True),
        "uuudd": sympy.symbols('c', real=True, positive=True, nonzero=True),
        "uudud": sympy.symbols('d', real=True, positive=True, nonzero=True),
        "uuddd": sympy.symbols('e', real=True, positive=True, nonzero=True),
        "udddd": sympy.symbols('f', real=True, positive=True, nonzero=True),
        "ddddd": sympy.symbols('g', real=True, positive=True, nonzero=True),
        "ddddu": sympy.symbols('h', real=True, positive=True, nonzero=True),
        "ddduu": sympy.symbols('i', real=True, positive=True, nonzero=True),
        "ddudu": sympy.symbols('j', real=True, positive=True, nonzero=True),
        "dduuu": sympy.symbols('k', real=True, positive=True, nonzero=True),
        "duuuu": sympy.symbols('l', real=True, positive=True, nonzero=True),
    }

    before.states = {
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

    movesets = enumerate_all_changes_in_pair_move()
    print

    moveset_index = 0

    final_probabilities = 0
    final_probabilities_corners = 0
    final_counts = {}

    for moveset in movesets:
        before_states, after_states = moveset

        # final_probabilities = 0
        # final_counts = 0

        probability_of_move_occuring = calculate_pair_probability(before, before_states)
        probability_of_move_occuring = probability_of_move_occuring[0] / probability_of_move_occuring[1]

        probability_of_move_occuring_corners = calculate_pair_probability_corners(before, before_states)
        probability_of_move_occuring_corners = (
            probability_of_move_occuring_corners[0] / probability_of_move_occuring_corners[1]
        )

        print(before_states, probability_of_move_occuring, probability_of_move_occuring_corners)
        print(calculate_pair_probability_corners(before, before_states))

        final_probabilities += probability_of_move_occuring
        final_probabilities_corners += probability_of_move_occuring_corners

        moveset_index += 1
    print(final_probabilities)
    print(sympy.simplify(final_probabilities))

    print(to_mathematica(final_probabilities_corners))
    print(sympy.simplify(final_probabilities_corners))

    exit(0)
