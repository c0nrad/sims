from ising_1d import Ising1D
import numpy as np
import matplotlib.pyplot as plot

from utils import ud_to_value, value_to_ud

N = 500
grid = Ising1D(N, 5000)

correct = []
grid.loop(1000000)

states = grid.count_normalized_states()


def get_next_spin_probabilistic(previous, states):
    if len(previous) != 2:
        raise Exception(previous + " should be length 2 string")

    possible_orientations = {"uuu": 1, "uud": 2, "duu": 2, "dud": 1, "ddd": 1, "ddu": 2, "udd": 2, "udu": 1}

    states["duu"] = states["uud"]
    states["udd"] = states["ddu"]

    out = {"u": 0, "d": 0}
    normalization = 0
    for state in states:
        if (previous[0] == "0" or previous[0] == state[0]) and (previous[1] == "0" or previous[1] == state[1]):
            out[state[2]] += states[state] / possible_orientations[state]
            normalization += states[state] / possible_orientations[state]

    return {k: v / normalization for (k, v) in out.items()}


# print(get_next_spin_probabilistic("uu", {"uuu": 1, "uud": 2, "dud": 0, "ddd": 0, "ddu": 0, "udu": 0}))
# assert get_next_spin_probabilistic("uu", {"uuu": 1, "uud": 2, "dud": 0, "ddd": 0, "ddu": 0, "udu": 0}) == {
#     "u": 0.5,
#     "d": 0.5,
# }


def pair_probabilities(states):
    out = {"uu": 0, "ud": 0, "du": 0, "dd": 0}
    normalization = 0
    for state in states:
        out[state[0] + state[1]] += states[state] / 2
        out[state[1] + state[2]] += states[state] / 2
        normalization += states[state]

    out = {k: v / normalization for (k, v) in out.items()}
    return out


# def generate_chain(L, states):
#     grid = Ising1D(L, 0)
#     grid.grid = np.zeros((L))

#     for i in range(L):
#         requirements = value_to_ud(grid.at(i - 2)) + value_to_ud(grid.at(i - 1))
# next_spin_probabilities = get_next_spin_probabilistic(requirements, states)

#         # print(next_spin_probabilities)
# next_spin = np.random.choice(list(next_spin_probabilities.keys()), p=list(next_spin_probabilities.values()))
#         grid.set(i, ud_to_value(next_spin))

#     return grid

# print(pair_probabilities(states))

multiplicity = 0
for (pair, p) in pair_probabilities(states).items():
    next_spin_probabilities = get_next_spin_probabilistic(pair, states)
    max_p = max(next_spin_probabilities.values())

    for (next_spin, next_spin_probability) in next_spin_probabilities.items():
        multiplicity += p * (1 / max_p)

print(multiplicity)

# grid2 = generate_chain(N, states)
# states2 = grid2.count_normalized_states()

# print("old", states)
# print("new", states2)
