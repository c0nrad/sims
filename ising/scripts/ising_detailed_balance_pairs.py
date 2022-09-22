from functools import reduce
import math
from builder import sympy_vector
from ising import Ising
import itertools
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


def enumerate_all_changes_in_pair_move():
    grid = Ising(5, 0)
    grid.grid = np.ones((5, 5))

    known_configs = []

    movesets = []
    for config in list(itertools.product([-1, 1], repeat=8)):

        grid.set(1, 0, config[0])
        grid.set(2, 0, config[1])

        grid.set(0, 1, config[2])
        grid.set(1, 1, config[3])
        grid.set(2, 1, config[4])
        grid.set(3, 1, config[5])

        grid.set(1, 2, config[6])
        grid.set(2, 2, config[7])

        before_states = get_pair_enumeration_states(grid)
        grid.set(1, 1, -1 * grid.at(1, 1))
        after_states = get_pair_enumeration_states(grid)

        movesets.append((before_states, after_states))

    return movesets


def enumerate_all_diagonal_pairs():
    grid = Ising(5, 0)
    grid.grid = np.ones((5, 5))

    known_configs = []

    movesets = []
    for config in list(itertools.product([-1, 1], repeat=8)):

        grid.set(2, 0, config[0])

        grid.set(1, 1, config[1])
        grid.set(2, 1, config[2])
        grid.set(3, 1, config[3])

        grid.set(0, 2, config[4])
        grid.set(1, 2, config[5])
        grid.set(2, 2, config[6])

        grid.set(1, 3, config[7])

        before_states = [grid.state_at(1, 2), grid.state_at(2, 1)]
        after_states = [grid.state_at(1, 2), grid.state_at(2, 1)]

        movesets.append((before_states, after_states))

    return movesets


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


def to_mathematica(i: str):

    out = re.sub(
        r"exp\(([t\d\/-]*)\)",
        r"Exp[\1]",
        str(i).replace("**", "^").replace("sqrt(2)", "Sqrt[2]"),
    )
    # print("to_mathematica", i, out)
    return out


# def calculate_reverse_pair_probability(state_vector, states_group):
#     middle_state = states_group[1]
#     left_state = states_group[0]

#     probability_of_move_occuring = count_unique_fits(middle_state, state_vector)

#     left_fits = count_unique_fits(middle_state[4] + "0" + middle_state[0] + "00", state_vector)
#     assert middle_state[0] == left_state[2]

#     probability_of_move_occuring *= count_unique_fits(left_state, state_vector) / left_fits
#     return probability_of_move_occuring


def calculate_diagonal_pair_probability(state_vector, states_group):
    middle_state = states_group[0]
    right_state = states_group[1]

    probability_of_move_occuring = count_unique_fits(middle_state, state_vector)

    right_fits = count_unique_fits("000" + middle_state[2] + middle_state[1], state_vector)
    assert middle_state[1] == right_state[4]
    assert middle_state[2] == right_state[3]

    probability_of_move_occuring *= count_unique_fits(right_state, state_vector)
    return (probability_of_move_occuring, right_fits)


def calculate_pair_probability(state_vector, states_group):
    middle_state = states_group[0]
    right_state = states_group[1]

    probability_of_move_occuring = count_unique_fits(middle_state, state_vector)

    right_fits = count_unique_fits(middle_state[2] + "000" + middle_state[0], state_vector)
    assert middle_state[0] == right_state[4]
    assert middle_state[2] == right_state[0]

    probability_of_move_occuring *= count_unique_fits(right_state, state_vector)
    return (probability_of_move_occuring, right_fits)


def calculate_pair_probability_corners(state_vector, states_group):
    middle_state = states_group[0]
    right_state = states_group[1]

    probability_of_move_occuring = count_unique_fits(middle_state, state_vector)

    top_right_fits = count_unique_fits("000" + middle_state[2] + middle_state[1], state_vector)
    probability_of_move_occuring *= count_unique_fits(
        right_state[1] + "00" + middle_state[2] + middle_state[1], state_vector
    )

    bottom_right_fits = count_unique_fits("0" + middle_state[2] + "00" + middle_state[3], state_vector)
    probability_of_move_occuring *= count_unique_fits(
        right_state[3] + middle_state[2] + "00" + middle_state[3], state_vector
    )

    far_right_fits = count_unique_fits(
        right_state[0] + right_state[1] + "0" + right_state[3] + right_state[4], state_vector
    )

    assert middle_state[0] == right_state[4]
    assert middle_state[2] == right_state[0]

    probability_of_move_occuring *= count_unique_fits(right_state, state_vector)
    return (probability_of_move_occuring, top_right_fits * bottom_right_fits * far_right_fits)


# assert (
#     calculate_pair_probability(sympy_vector(), ["ddddd", "dddud"]) == "g*h/(4*(g + 3*h/4 + i/2 + j/2 + k/4))"
# ), calculate_pair_probability(sympy_vector(), ["ddddd", "dddud"])


def print_pair(middle, right):
    print(" " + middle[1] + right[1])
    print(middle[4] + middle[0] + middle[2] + right[2])
    print(" " + middle[3] + right[3])


def energy_difference(before, after):
    before_middle = ud_to_value(before[0])
    after_middle = ud_to_value(after[0])
    e_before = sum([before_middle * ud_to_value(s) for s in before[1:]])
    e_after = sum([after_middle * ud_to_value(s) for s in after[1:]])

    return e_after - e_before


assert energy_difference("udddd", "ddddd") == 8
assert energy_difference("uduud", "dduud") == 0
assert energy_difference("uduuu", "dduuu") == -4


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

    # print(before.calculate_simple_correlation_distance())
    # exit(1)

    t = sympy.symbols('t', real=True, positive=True, nonzero=True)

    subs = {
        before.states['duuuu']: before.states['uuuuu'] * sympy.exp(-8 / t),
        before.states['ddddd']: before.states['udddd'] * sympy.exp(8 / t),
        before.states['dduuu']: before.states['uuuud'] * sympy.exp(-4 / t),
        before.states['ddddu']: before.states['uuddd'] * sympy.exp(4 / t),
        before.states['ddduu']: before.states['uuudd'],
        before.states['ddudu']: before.states['uudud'],
        # t: 1 / sympy.log(sympy.sqrt(2) + 1),
        # t: sympy.log(20),
    }

    after = before.clone()

    movesets = enumerate_all_changes_in_pair_move()

    moveset_index = 0

    sanity_before = []
    sanity_after = []

    equal_ds = {}

    for moveset in movesets:
        print("=========")

        print(moveset_index, len(movesets))
        before_states, after_states = moveset

        before_clone = before.clone()
        after_clone = before.clone()

        print("Before", before_states)
        print_pair(before_states[0], before_states[1])

        print("After", after_states)
        print_pair(after_states[0], after_states[1])

        probability_of_move_occuring_n, probability_of_move_occuring_d = calculate_pair_probability(
            before_clone, before_states
        )
        probability_of_opposite_move_occuring_n, probability_of_opposite_move_occuring_d = calculate_pair_probability(
            after_clone, after_states
        )

        print(probability_of_move_occuring_n)
        print(probability_of_move_occuring_d)
        print(probability_of_opposite_move_occuring_n)
        print(probability_of_opposite_move_occuring_d)

        sanity_before.append(probability_of_move_occuring_n / probability_of_move_occuring_d)
        sanity_after.append(probability_of_opposite_move_occuring_n / probability_of_opposite_move_occuring_d)

        dE = energy_difference(before_states[0], after_states[0])

        print("dE=", dE)

        if dE < 0:
            probability_of_move_occuring_n *= sympy.exp(dE / t)
        elif dE > 0:
            probability_of_opposite_move_occuring_n *= sympy.exp(-dE / t)

        print("Finals")
        print(probability_of_move_occuring_n)
        print(probability_of_opposite_move_occuring_n)

        # eqn = (
        #     probability_of_move_occuring_n
        #     * probability_of_opposite_move_occuring_d
        #     / probability_of_opposite_move_occuring_n
        #     - probability_of_move_occuring_d
        # )

        if probability_of_move_occuring_d / probability_of_opposite_move_occuring_d not in equal_ds:
            equal_ds[probability_of_move_occuring_d / probability_of_opposite_move_occuring_d] = [
                to_mathematica((probability_of_move_occuring_n / probability_of_opposite_move_occuring_n).subs(subs))
            ]
        else:
            equal_ds[probability_of_move_occuring_d / probability_of_opposite_move_occuring_d].append(
                to_mathematica((probability_of_move_occuring_n / probability_of_opposite_move_occuring_n).subs(subs))
            )

        # eqn = eqn.subs(subs).subs(subs)
        # print(eqn)
        # print(sympy.simplify(eqn))
        # print("ice")
        # print(to_mathematica(eqn))
        # equations.append(eqn)

        moveset_index += 1

    assert str(sympy.simplify(sum(sanity_before))) == "a + b + c + d + e + f + g + h + i + j + k + l"
    assert str(sympy.simplify(sum(sanity_after))) == "a + b + c + d + e + f + g + h + i + j + k + l"

    out = ""
    for eqn in equal_ds:
        print("====")
        print(eqn)
        out += ("==".join(equal_ds[eqn])) + " &&"

    print("tehe")
    print(out)

    for eqn in equal_ds:
        print("====")
        print(to_mathematica(eqn.subs(subs)) + "==" + equal_ds[eqn][0])

    # print(equal_ds)

    # base_assumptions = "T > 0 && 0 < a < 1 && 0 < b < 1 && 0 < c < 1 && 0 < d < 1 && 0 < e < 1 && 0 < f < 1"

    # random.shuffle(equations)
    # mathematica_expression = "FindRoot[{" + to_mathematica(total_probability.subs(subs).subs(subs)) + " == 0, "
    # for eqn in equations[:6]:
    #     mathematica_expression += to_mathematica(eqn) + " == 0,"
    # mathematica_expression = mathematica_expression[0:-1] + "}, {{a, .25},{b, .1},{c, .1},{d, .1},{e, .1},{f, .1}}]"
    # print(mathematica_expression)

    # assert sympy.simplify(sum(sanity_sum)) == 0

    # base_assumptions_equal = (
    #     "0 < t < Infinity && 0 <= a <= 1 && 0 <= b <= 1 && 0 <= c <= 1 && 0 <= d <= 1 && 0 <= e <= 1 && 0 <= f <= 1"
    # )

    # base_assumptions = "0 < t < Infinity && 0 < a < 1 && 0 < b < 1 && 0 < c < 1 && 0 < d < 1 && 0 < e < 1 && 0 < f < 1"

    # mathematica_expression = "Reduce[" + base_assumptions + " && "
    # for eqn in equations:
    #     mathematica_expression += to_mathematica(eqn) + " == 0 &&"
    # mathematica_expression = mathematica_expression[0:-2] + ", {a,b,c,d,e,f}, PositiveReals]"
    # print(mathematica_expression)

    # out_file = open("ising_equil_large_system.txt", "w")
    # out_file.write(str(mathematica_expression))
    # out_file.close()

    # out = sympy.solve(
    #     equations,
    #     [
    #         before.states['uuuuu'],
    #         before.states['uuuud'],
    #         before.states['uuudd'],
    #         before.states['uudud'],
    #         before.states['uuddd'],
    #         before.states['udddd'],
    #         # before.states['ddddd'],
    #         # before.states['ddddu'],
    #         # before.states['ddduu'],
    #         # before.states['ddudu'],
    #         # before.states['dduuu'],
    #         # before.states['duuuu'],
    #         # t,
    #     ],
    # )
