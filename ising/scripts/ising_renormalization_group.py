from functools import reduce
import math
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


def enumerate_all_group_moves():
    grid = Ising(5, 0)
    grid.grid = np.ones((5, 5))

    movesets = []
    for config in list(itertools.product([-1, 1], repeat=13)):
        grid.set(0, 2, config[0])

        grid.set(1, 1, config[1])
        grid.set(1, 2, config[2])
        grid.set(1, 3, config[3])

        grid.set(2, 0, config[4])
        grid.set(2, 1, config[5])
        grid.set(2, 2, config[6])
        grid.set(2, 3, config[7])
        grid.set(2, 4, config[8])

        grid.set(3, 1, config[9])
        grid.set(3, 2, config[10])
        grid.set(3, 3, config[11])
        grid.set(4, 2, config[12])

        before_states = get_enumeration_states(grid)
        grid.set(2, 2, -1 * grid.at(2, 2))
        after_states = get_enumeration_states(grid)

        movesets.append((before_states, after_states))

    return movesets


def get_enumeration_states(grid):
    states = []
    for middle in [(2, 2), (2, 1), (3, 2), (2, 3), (1, 2)]:
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


def energy_difference(before, after):
    before_middle = ud_to_value(before[0])
    after_middle = ud_to_value(after[0])
    e_before = sum([before_middle * ud_to_value(s) for s in before[1:]])
    e_after = sum([after_middle * ud_to_value(s) for s in after[1:]])

    return e_after - e_before


def calculate_group_probability(state_vector, states_group):
    probability_of_move_occuring_n = count_unique_fits(states_group[0], state_vector)

    middle_state = states_group[0]
    top_state = states_group[1]
    right_state = states_group[2]
    bottom_state = states_group[3]
    left_state = states_group[4]

    top_fits = count_unique_fits(middle_state[1] + "00" + middle_state[0] + "0", state_vector)
    right_fits = count_unique_fits(middle_state[2] + top_state[2] + "00" + middle_state[0], state_vector)
    bottom_fits = count_unique_fits(middle_state[3] + middle_state[0] + right_state[3] + "00", state_vector)
    left_fits = count_unique_fits(
        middle_state[4] + top_state[4] + middle_state[0] + bottom_state[4] + "0", state_vector
    )

    assert (
        middle_state[0] == top_state[3]
        and top_state[3] == right_state[4]
        and right_state[4] == bottom_state[1]
        and bottom_state[1] == left_state[2]
    )

    probability_of_move_occuring_n *= count_unique_fits(top_state, state_vector)
    probability_of_move_occuring_n *= count_unique_fits(right_state, state_vector)
    probability_of_move_occuring_n *= count_unique_fits(bottom_state, state_vector)
    probability_of_move_occuring_n *= count_unique_fits(left_state, state_vector)
    return (probability_of_move_occuring_n, top_fits * right_fits * bottom_fits * left_fits)


def majority(state):
    if state.count("u") > state.count("d"):
        return "u"
    if state.count("u") == state.count("d"):
        raise Exception("invalid state")
    return "d"


def get_renormalized_state(states):
    return normalize_state("".join([majority(s) for s in states]))


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

    t = sympy.symbols('t')

    subs = {
        before.states['duuuu']: before.states['uuuuu'] * sympy.exp(-8 / t),
        before.states['ddddd']: before.states['udddd'] * sympy.exp(8 / t),
        before.states['dduuu']: before.states['uuuud'] * sympy.exp(-4 / t),
        before.states['ddddu']: before.states['uuddd'] * sympy.exp(4 / t),
        before.states['ddduu']: before.states['uuudd'],
        before.states['ddudu']: before.states['uudud'],
    }

    after = before.clone()

    movesets = enumerate_all_group_moves()

    # random.shuffle(movesets)

    moveset_index = 0

    sanity_before = []

    eqns = []
    final_state_eqn = {}

    for moveset in movesets:
        # print("=========")

        print(moveset_index, len(movesets))
        before_states, after_states = moveset

        before_clone = before.clone()

        # print("Before", before_states)
        # print("After", after_states)

        probability_of_move_occuring_n, probability_of_move_occuring_d = calculate_group_probability(
            before_clone, before_states
        )

        # print(probability_of_move_occuring_n)
        # print(probability_of_move_occuring_d)
        # print(probability_of_opposite_move_occuring_n)
        # print(probability_of_opposite_move_occuring_d)

        # sanity_before.append(probability_of_move_occuring_n / probability_of_move_occuring_d)
        # eqns.append(probability_of_move_occuring_n / probability_of_move_occuring_d)

        # print(probability_of_move_occuring_n)
        # print(probability_of_move_occuring_d)

        # print("Finals")
        # print(probability_of_move_occuring_n)
        # print(probability_of_opposite_move_occuring_n)

        # eqn = (
        #     probability_of_move_occuring_n
        #     * probability_of_opposite_move_occuring_d
        #     / probability_of_opposite_move_occuring_n
        #     - probability_of_move_occuring_d
        # )

        final_state = get_renormalized_state(before_states)

        if final_state not in final_state_eqn:
            final_state_eqn[final_state] = [
                to_mathematica((probability_of_move_occuring_n / probability_of_move_occuring_d).subs(subs))
            ]
        else:
            final_state_eqn[final_state].append(
                to_mathematica((probability_of_move_occuring_n / probability_of_move_occuring_d).subs(subs))
            )

        # # eqn = eqn.subs(subs).subs(subs)
        # # print(eqn)
        # # print(sympy.simplify(eqn))
        # # print("ice")
        # # print(to_mathematica(eqn))
        # # equations.append(eqn)

        moveset_index += 1

    # assert str(sympy.simplify(sum(sanity_before))) == "a + b + c + d + e + f + g + h + i + j + k + l"
    # assert str(sympy.simplify(sum(sanity_after))) == "a + b + c + d + e + f + g + h + i + j + k + l"

    # sanity_out = "+".join([to_mathematica(eqn) for eqn in sanity_before])
    # print(sanity_out)
    # # for eqn in sanity_before:
    #     print("====")
    #     print(eqn)
    #     sanity_out += ("==".join(equal_eqn_map[eqn])) + " &&"
    # print(sanity_out)
    # exit(1)

    print("+".join(final_state_eqn["uuuuu"]))
    exit(1)

    out = "Reduce["

    for state in final_state_eqn:
        out += str(to_mathematica(before.states[state].subs(subs))) + " == " + "+".join(final_state_eqn[state]) + "&&"

    print(out)

    out_file = open("ising_renormalizatoin_group_sln.txt", "w")
    out_file.write(str(out))
    out_file.close()

    # out = "+".join([to_mathematica(eqn.subs(subs)) for eqn in eqns])
    # out += "== a + b + c + d + e + f"
    # print(out)
    # for eqn in :
    #     print("====")
    #     print(eqn)
    #     out += ("==".join(equal_eqn_map[eqn])) + " &&"

    # print("tehe")
    # print(out)

    # for eqn in equal_eqn_map:
    #     print("====")
    #     print(to_mathematica(eqn.subs(subs)) + "==" + equal_eqn_map[eqn][0])

    # delta = before.clone()
    # # equations = []
    # for state in after.states:
    #     delta.states[state] = after.states[state] - before.states[state]
    #     # equations.append(sympy.Eq(delta.states[state], 0))

    # out = sympy.nonlinsolve(
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
    #         # T,
    #     ],
    # )

    # print(out)

    # base_assumptions = "T > 0 && a > 0 && b > 0 && c > 0 && d > 0 && e > 0 && f > 0"

    # mathematica_expression = "Solve[" + base_assumptions + " && "
    # for eqn in equations:
    #     mathematica_expression += to_mathematica(eqn) + " == 0 &&"
    # mathematica_expression = mathematica_expression[0:-2] + ", {a,b,c,d,e,f}, Reals]"
    # print(mathematica_expression)

    # mathematica_expression = "Solve["
    # for state in after.states:
    #     mathematica_expression += to_mathematica(delta.states[state])[0] + " +"
    # mathematica_expression = mathematica_expression[0:-1] + "]"
    # print(mathematica_expression)

    # out_file = open("ising_equil_large_system.txt", "w")
    # out_file.write(str(mathematica_expression))
    # out_file.close()

    # print("Equations", equations)
    # out = sympy.nonlinsolve(
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
    #         # T,
    #     ],
    # )

    # print(out)
    # print("")
    # print("delta_dsitance", delta_distance)
    # print("")

    # f_diff = open("results_after_diff.txt", "w")
    # out = sympy.diff(delta_distance, T)
    # print("After diff", out)
    # f_diff.write(str(out))
    # f_diff.close()
    # print("")

    # # out = sympy.integrate(out, (sympy.symbols('a'), 0, 0.5))
    # # print("after int")

    # f_simp = open("results_after_simp.txt", "w")
    # out = sympy.simplify(out)
    # print("After simplify", out)
    # f_simp.write(str(out))
    # f_simp.close()
    # print("")

    # f_solve = open("results_after_solve.txt", "w")
    # critical_t = sympy.solve([out, sympy.Eq(all_states, 1)], T)
    # print("Critical_t", critical_t)
    # f_solve.write(str(critical_t))
    # f_solve.close()
    # # f.close()
