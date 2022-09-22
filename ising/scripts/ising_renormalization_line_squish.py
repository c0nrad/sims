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
from ising_renormalization_line import enumerate_all_states, get_line_groups, duplication_map


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
    if state.count("u") > state.count("d"):
        return "u"
    if state.count("u") == state.count("d"):
        raise Exception("invalid state")
    return "d"


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

    t = sympy.symbols('t')

    subs = {
        before.states['duuuu']: before.states['uuuuu'] * sympy.exp(-8 / t),
        before.states['ddddd']: before.states['udddd'] * sympy.exp(8 / t),
        before.states['dduuu']: before.states['uuuud'] * sympy.exp(-4 / t),
        before.states['ddddu']: before.states['uuddd'] * sympy.exp(4 / t),
        before.states['ddduu']: before.states['uuudd'],
        before.states['ddudu']: before.states['uudud'],
    }

    mapping = {}
    total = 0

    line_groups = get_line_groups(before)
    final_line_group = {}
    for state in enumerate_all_states():
        final_line = majority(state[4] + state[0] + state[2])
        if final_line not in final_line_group:
            final_line_group[final_line] = 0

        final_line_group[final_line] += before.states[normalize_state(state)] / duplication_map[normalize_state(state)]

print("Line Groups", line_groups)
print("Final line group", final_line_group)

print("Line group sum", sum(line_groups.values()))
print("Final group sum", sum(final_line_group.values()))

out = ""
for line in final_line_group:
    out += (
        to_mathematica(final_line_group[line].subs(subs)) + "==" + to_mathematica(line_groups[line].subs(subs)) + "&&"
    )
    print(
        line,
        final_line_group[line],
        "==",
        line_groups[line],
    )

print(out)
