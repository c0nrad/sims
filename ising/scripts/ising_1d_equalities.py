from ising_1d_chains import get_next_spin_probabilistic, get_next_spin_probabilistic_normalized
from ising_detailed_balance_pairs import to_mathematica
from utils import ud_to_value, value_to_ud

import sympy
import itertools

states = {
    "uuu": sympy.symbols('a', real=True, positive=True, nonzero=True),
    "uud": sympy.symbols('b', real=True, positive=True, nonzero=True),
    "dud": sympy.symbols('c', real=True, positive=True, nonzero=True),
    "ddd": sympy.symbols('a', real=True, positive=True, nonzero=True),
    "ddu": sympy.symbols('b', real=True, positive=True, nonzero=True),
    "udu": sympy.symbols('c', real=True, positive=True, nonzero=True),
}

t = sympy.symbols('t', real=True, positive=True, nonzero=True)


def energy_difference_line(before, after):
    eBefore = 0
    eAfter = 0
    for i in range(len(before)):
        if before[i] == before[(i + 1) % len(before)]:
            eBefore -= 1
        else:
            eBefore += 1

        if after[i] == after[(i + 1) % len(after)]:
            eAfter -= 1
        else:
            eAfter += 1

    return eAfter - eBefore


assert energy_difference_line("uuuuu", "uuduu") == 4

out = ""
possible_orientations = {"uuu": 1, "uud": 2, "duu": 2, "dud": 1, "ddd": 1, "ddu": 2, "udd": 2, "udu": 1}

denom_grouping = {}

for config in list(itertools.product([-1, 1], repeat=5)):
    line = "".join([value_to_ud(a) for a in config])

    p_before = (
        states[line[0] + line[1] + line[2]]
        / possible_orientations[line[0] + line[1] + line[2]]
        * get_next_spin_probabilistic(line[1] + line[2], states)[line[3]]
        * get_next_spin_probabilistic(line[2] + line[3], states)[line[4]]
    )

    line_after = line[0] + line[1] + ("u" if line[2] == "d" else "d") + line[3] + line[4]
    # line_after[2] = "u" if line[2] == "d" else "d"
    p_after = (
        states[line_after[0] + line_after[1] + line_after[2]]
        / possible_orientations[line_after[0] + line_after[1] + line_after[2]]
        * get_next_spin_probabilistic(line_after[1] + line_after[2], states)[line_after[3]]
        * get_next_spin_probabilistic(line_after[2] + line_after[3], states)[line_after[4]]
    )

    dE = energy_difference_line(line, line_after)
    # if dE == 0:
    # print(line, line_after, dE, p_before, "==", p_after)
    if dE != 0:
        p_before *= sympy.exp(-dE / t)

    p_before_n, p_before_d = p_before.as_numer_denom()
    p_after_n, p_after_d = p_after.as_numer_denom()

    if (p_after_d) not in denom_grouping:
        denom_grouping[p_after_d] = []

    if p_before_d * p_after_n / p_before_n not in denom_grouping[p_after_d]:
        denom_grouping[p_after_d].append(p_before_d * p_after_n / p_before_n)

    print(p_before_n / p_before_d, "=", p_after_n / p_after_d)

    # print(line, line_after, p_before, p_after)
    # out += to_mathematica(p_before) + " == " + to_mathematica(p_after) + "&&"
    # get_next_spin_probabilistic_normalized


for denom in denom_grouping:
    print("Reduce[", to_mathematica(denom), "==", to_mathematica(denom_grouping[denom][0]), ", PositiveReals]")
    # print("==".join([to_mathematica(a) for a in denom_grouping[denom]]))
    print("\n\n")

print("t>0&&" + out[0:-2])
