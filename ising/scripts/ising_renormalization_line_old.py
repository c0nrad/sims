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
from math import sqrt


def enumerate_all_states():
    grid = Ising(5, 0)
    grid.grid = np.ones((3, 3))

    lines = []
    for config in list(itertools.product([-1, 1], repeat=5)):
        grid.set(1, 0, config[0])

        grid.set(0, 1, config[1])
        grid.set(1, 1, config[2])
        grid.set(2, 1, config[3])

        grid.set(1, 2, config[4])

        before_states = get_enumeration_states(grid)

        lines.append(before_states)
    print(len(lines))

    return lines


def get_enumeration_states(grid):
    states = []
    for middle in [(1, 1)]:
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
    return states[0]


def to_mathematica(i: str):

    out = re.sub(
        r"exp\(([t\d\/-]*)\)",
        r"Exp[\1]",
        str(i).replace("**", "^").replace("sqrt(2)", "Sqrt[2]"),
    )
    # print("to_mathematica", i, out)
    return out


def majority(state):
    if len(state) != 2:
        raise Exception(state)
    if state.count("u") > state.count("d"):
        return "u"
    if state.count("u") == state.count("d"):
        return state[0]
    return "d"


duplication_map = {
    "uuuuu": 1,
    "uuuud": 4,
    "uuudd": 4,
    "uudud": 2,
    "uuddd": 4,
    "udddd": 1,
    "ddddd": 1,
    "ddddu": 4,
    "ddduu": 4,
    "ddudu": 2,
    "dduuu": 4,
    "duuuu": 1,
}


def get_line_groups(state_vector):
    line_groups = {}
    t_p = 0
    for state in enumerate_all_states():
        print(state)
        hor_line = state[4] + state[0] + state[2]
        ver_line = state[1] + state[0] + state[3]
        hor_line2 = state[2] + state[0] + state[4]
        ver_line2 = state[3] + state[0] + state[1]

        for l in [hor_line, ver_line, hor_line2, ver_line2]:
            if l not in line_groups:
                line_groups[l] = 0

            line_groups[l] += state_vector.states[normalize_state(state)] / 4 / duplication_map[normalize_state(state)]
            t_p += state_vector.states[normalize_state(state)] / 4 / duplication_map[normalize_state(state)]

    return line_groups


def get_renormalized_lines(line):
    out = [""]

    for i in range(0, 6, 2):
        if line[i] == line[i + 1]:
            out = [a + line[i] for a in out]
        else:
            new_out = []
            for a in out:
                new_out.append(a + "u")
                new_out.append(a + "d")

            out = new_out

    return out


assert get_renormalized_lines("uudduu") == ["udu"], get_renormalized_lines("uudduu")
assert get_renormalized_lines("uduudd") == ["uud", "dud"], get_renormalized_lines("uduudd")
assert get_renormalized_lines("ududud") == [
    'uuu',
    'uud',
    'udu',
    'udd',
    'duu',
    'dud',
    'ddu',
    'ddd',
], get_renormalized_lines("ududud")

if __name__ == "__main__":

    before = IsingStateVector(None)

    # before.states = {
    #     "uuuuu": sympy.symbols('a', real=True, positive=True, nonzero=True),
    #     "uuuud": sympy.symbols('b', real=True, positive=True, nonzero=True),
    #     "uuudd": sympy.symbols('c', real=True, positive=True, nonzero=True),
    #     "uudud": sympy.symbols('d', real=True, positive=True, nonzero=True),
    #     "uuddd": sympy.symbols('e', real=True, positive=True, nonzero=True),
    #     "udddd": sympy.symbols('f', real=True, positive=True, nonzero=True),
    #     "ddddd": sympy.symbols('a', real=True, positive=True, nonzero=True),
    #     "ddddu": sympy.symbols('b', real=True, positive=True, nonzero=True),
    #     "ddduu": sympy.symbols('c', real=True, positive=True, nonzero=True),
    #     "ddudu": sympy.symbols('d', real=True, positive=True, nonzero=True),
    #     "dduuu": sympy.symbols('e', real=True, positive=True, nonzero=True),
    #     "duuuu": sympy.symbols('f', real=True, positive=True, nonzero=True),
    # }

    # before.states = {
    #     "uuuuu": 1 / 8,
    #     "uuuud": 1 / sqrt(2) - 1 / 2,
    #     "uuudd": 3 / 2 - sqrt(2),
    #     "uudud": 3 / 4 - 1 / sqrt(2),
    #     "uuddd": 5 / sqrt(2) - 7 / 2,
    #     "udddd": 17 / 8 - 3 / sqrt(2),
    #     "ddddd": 1 / 8,
    #     "ddddu": 1 / sqrt(2) - 1 / 2,
    #     "ddduu": 3 / 2 - sqrt(2),
    #     "ddudu": 3 / 4 - 1 / sqrt(2),
    #     "dduuu": 5 / sqrt(2) - 7 / 2,
    #     "duuuu": 17 / 8 - 3 / sqrt(2),
    # }

    before.states = {
        'uuuuu': 0.31860382827454153,
        'uuuud': 0.11006524473612249,
        'uuudd': 0.033584522832923146,
        'uudud': 0.006982608695652079,
        'uuddd': 0.019013016133442816,
        'udddd': 0.009498878862455491,
        'ddddd': 0.32248706590101117,
        'ddddu': 0.11092879409351909,
        'ddduu': 0.03359819524200149,
        'ddudu': 0.006975170905113386,
        'dduuu': 0.018892152037189084,
        'duuuu': 0.009370522286026702,
    }

    t = sympy.symbols('t')

    subs = {
        before.states['duuuu']: before.states['uuuuu'] * sympy.exp(-8 / t),
        before.states['ddddd']: before.states['udddd'] * sympy.exp(8 / t),
        before.states['dduuu']: before.states['uuuud'] * sympy.exp(-4 / t),
        before.states['ddddu']: before.states['uuddd'] * sympy.exp(4 / t),
        before.states['ddduu']: before.states['uuudd'],
        before.states['ddudu']: before.states['uudud'],
        before.states['udddd']: before.states['uuuuu'] * sympy.exp(-8 / t),
        before.states['uuddd']: before.states['uuuud'] * sympy.exp(-4 / t),
        t: 2 / sympy.log(sympy.sqrt(2) + 1),
    }

    line_groups = get_line_groups(before)

    final_groups = {}
    sanity = 0

    for config in list(itertools.product([-1, 1], repeat=6)):
        line = [value_to_ud(v) for v in config]
        p = count_unique_fits(line[1] + "0" + line[2] + "0" + line[0], before)

        # Spot 2
        p /= count_unique_fits(line[2] + "000" + line[1], before)
        p *= count_unique_fits(line[2] + "0" + line[3] + "0" + line[1], before)

        # Spot 3
        p /= count_unique_fits(line[3] + "000" + line[2], before)
        p *= count_unique_fits(line[3] + "0" + line[4] + "0" + line[2], before)

        # Spot 4
        p /= count_unique_fits(line[4] + "000" + line[3], before)
        p *= count_unique_fits(line[4] + "0" + line[5] + "0" + line[3], before)

        print(line, get_renormalized_lines(line))

        normalized_lines = get_renormalized_lines(line)
        for n_line in normalized_lines:
            if n_line not in final_groups:
                final_groups[n_line] = 0

            final_groups[n_line] += p / len(normalized_lines)

        sanity += p

    # print("Sanity", sympy.simplify(sanity))

    print("Line Groups", line_groups)
    print("Final line group", final_groups)

    print("Line group sum", sum(line_groups.values()))
    print("Final group sum", sum(final_groups.values()))

    out = ""
    for line in final_groups:
        # out += (
        #     to_mathematica(final_groups[line].subs(subs).subs(subs))
        #     + "=="
        #     + to_mathematica(line_groups[line].subs(subs).subs(subs))
        #     + "&&"
        # )
        print(line, "Final", final_groups[line], ", Expected?", line_groups[line])

    print(out)
