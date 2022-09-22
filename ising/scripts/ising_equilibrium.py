from functools import reduce
import math
from ising import Ising
import itertools
from ising_state_vector import IsingStateVector, normalize_state
import numpy as np
from utils import ud_to_value, value_to_ud
import sympy
import pdb
from pprint import pprint


def enumerate_all_changes_in_move():
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
    for middle in [(2, 2), (1, 2), (2, 1), (2, 3), (3, 2)]:
        x = middle[0]
        y = middle[1]
        state = (
            grid.at(x, y),
            grid.at(x, y - 1),
            grid.at(x + 1, y),
            grid.at(x, y + 1),
            grid.at(x - 1, y),
        )

        state = "".join([value_to_ud(a) for a in state])
        states.append(normalize_state(state))
    return states


def to_mathematica(i: str):
    return (
        str(i)
        .replace("**", "^")
        .replace("exp(-8/T)", "Exp[-8/T]")
        .replace("exp(-4/T)", "Exp[-4/T]")
        .replace("sqrt(2)", "Sqrt[2]"),
    )


if __name__ == "__main__":
    before = IsingStateVector(None)
    # before.states = {
    #     "uuuuu": sympy.symbols('a'),
    #     "uuuud": sympy.symbols('b'),
    #     "uuudd": sympy.symbols('c'),
    #     "uudud": sympy.symbols('d'),
    #     "uuddd": sympy.symbols('e'),
    #     "udddd": sympy.symbols('f'),
    #     "ddddd": sympy.symbols('g'),
    #     "ddddu": sympy.symbols('h'),
    #     "ddduu": sympy.symbols('i'),
    #     "ddudu": sympy.symbols('j'),
    #     "dduuu": sympy.symbols('k'),
    #     "duuuu": sympy.symbols('l'),
    # }

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

    all_states = sum(before.states.values())

    after = before.clone()
    epsilon = sympy.symbols('epsilon')
    T = sympy.symbols('T')

    movesets = enumerate_all_changes_in_move()
    moveset_index = 0

    equations = []

    for moveset in movesets:
        print(moveset_index, len(movesets))
        before_states, after_states = moveset

        before_clone = before.clone()
        after_clone = before.clone()
        probability_of_move_occuring = 1
        for before_state in before_states:
            probability_of_move_occuring *= before_clone.states[before_state]
            # before_clone.states[before_state] -= epsilon

        probability_of_opposite_move_occuring = 1
        for after_state in after_states:
            probability_of_opposite_move_occuring *= after_clone.states[after_state]

        before_middle = ud_to_value(before_states[0][0])
        after_middle = ud_to_value(after_states[0][0])
        e_before = sum([before_middle * ud_to_value(s) for s in before_states[0][1:]])
        e_after = sum([after_middle * ud_to_value(s) for s in after_states[0][1:]])

        dE = e_after - e_before

        if dE > 0:
            probability_of_move_occuring *= sympy.exp(-dE / T)
        else:
            probability_of_opposite_move_occuring *= sympy.exp(dE / T)

        eqn = probability_of_move_occuring - probability_of_opposite_move_occuring
        eqn = sympy.simplify(eqn)
        print(eqn)
        equations.append(eqn)
        # print(probability_of_move_occuring, "=", probability_of_opposite_move_occuring)

        # for i in range(5):
        #     after.states[before_states[i]] -= probability_of_move_occuring
        #     after.states[after_states[i]] += probability_of_move_occuring

        moveset_index += 1

    # delta = before.clone()
    # # equations = []
    # for state in after.states:
    #     delta.states[state] = after.states[state] - before.states[state]
    #     # equations.append(sympy.Eq(delta.states[state], 0))

    out = sympy.nonlinsolve(
        equations,
        [
            before.states['uuuuu'],
            before.states['uuuud'],
            before.states['uuudd'],
            before.states['uudud'],
            before.states['uuddd'],
            before.states['udddd'],
            # before.states['ddddd'],
            # before.states['ddddu'],
            # before.states['ddduu'],
            # before.states['ddudu'],
            # before.states['dduuu'],
            # before.states['duuuu'],
            # T,
        ],
    )

    print(out)

    base_assumptions = "a >= 0 && b >= 0 && c >= 0 && d >= 0 && e >= 0 && f >= 0 && g >= 0 && h >= 0 && i >= 0 && j >= 0 && k >= 0 && l >= 0 && c == i && d == j && a*Exp[-8/T] == l && g*Exp[-8/T] == f && b*Exp[-4/T] == k && h*Exp[-4/T] == e"

    mathematica_expression = "Solve[" + base_assumptions + " && "
    for eqn in equations:
        mathematica_expression += to_mathematica(eqn)[0] + " == 0 &&"
    mathematica_expression = mathematica_expression[0:-2] + ", {a}, Reals]"
    print(mathematica_expression)

    # mathematica_expression = "Solve["
    # for state in after.states:
    #     mathematica_expression += to_mathematica(delta.states[state])[0] + " +"
    # mathematica_expression = mathematica_expression[0:-1] + "]"
    # print(mathematica_expression)

    out_file = open("ising_equil_large_system.txt", "w")
    out_file.write(str(mathematica_expression))
    out_file.close()

    # print("Equations", equations)
    # print(sympy.nonlinsolve(equations, sympy.symbols('a b c d e f g h i j k l')))

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
