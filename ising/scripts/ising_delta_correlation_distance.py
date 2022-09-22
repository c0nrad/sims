from functools import reduce
from ising import Ising
import itertools
from ising_state_vector import IsingStateVector, normalize_state
import numpy as np
from utils import ud_to_value, value_to_ud
import sympy


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


if __name__ == "__main__":
    before = IsingStateVector(None)
    before.states = {
        "uuuuu": sympy.symbols('a'),
        "uuuud": sympy.symbols('b'),
        "uuudd": sympy.symbols('c'),
        "uudud": sympy.symbols('d'),
        "uuddd": sympy.symbols('e'),
        "udddd": sympy.symbols('f'),
        "ddddd": sympy.symbols('a'),
        "ddddu": sympy.symbols('b'),
        "ddduu": sympy.symbols('c'),
        "ddudu": sympy.symbols('d'),
        "dduuu": sympy.symbols('e'),
        "duuuu": sympy.symbols('f'),
    }

    all_states = sum(before.states.values())

    after = before.clone()

    epsilon = sympy.symbols('epsilon')
    T = sympy.symbols('T')

    movesets = enumerate_all_changes_in_move()
    moveset_index = 0

    for moveset in movesets:
        print(moveset_index, len(movesets))
        before_states, after_states = moveset

        # Since the board is infnite, I don't think we need to subtract epsilon for re-used states?
        probability_of_move_occuring = (
            before.states[before_states[0]]
            * before.states[before_states[1]]
            * before.states[before_states[2]]
            * before.states[before_states[3]]
            * before.states[before_states[4]]
        )

        before_middle = ud_to_value(before_states[0][0])
        after_middle = ud_to_value(after_states[0][0])
        e_before = sum([before_middle * ud_to_value(s) for s in before_states[0][1:]])
        e_after = sum([after_middle * ud_to_value(s) for s in after_states[0][1:]])

        dE = e_after - e_before

        if dE > 0:
            probability_of_move_occuring *= sympy.exp(-dE / T)

        for i in range(5):
            after.states[before_states[i]] -= epsilon * probability_of_move_occuring
            after.states[after_states[i]] += epsilon * probability_of_move_occuring

        moveset_index += 1

    delta_distance = (
        before.calculate_simple_correlation_distance()
        - before.calculate_total_magnetism()
        - after.calculate_simple_correlation_distance()
        + after.calculate_total_magnetism()
    )

    print("")
    print("delta_dsitance", delta_distance)
    print("")

    f_diff = open("results_after_diff.txt", "w")
    out = sympy.diff(delta_distance, T)
    print("After diff", out)
    f_diff.write(str(out))
    f_diff.close()
    print("")

    # out = sympy.integrate(out, (sympy.symbols('a'), 0, 0.5))
    # print("after int")

    f_simp = open("results_after_simp.txt", "w")
    out = sympy.simplify(out)
    print("After simplify", out)
    f_simp.write(str(out))
    f_simp.close()
    print("")

    f_solve = open("results_after_solve.txt", "w")
    critical_t = sympy.solve([out, sympy.Eq(all_states, 1)], T)
    print("Critical_t", critical_t)
    f_solve.write(str(critical_t))
    f_solve.close()
    # f.close()
