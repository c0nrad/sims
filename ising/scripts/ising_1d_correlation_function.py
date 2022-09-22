from ising_1d import Ising1D
import numpy as np
import matplotlib.pyplot as plot

from utils import ud_to_value, value_to_ud


def pair_probabilities(states):
    out = {"uu": 0, "ud": 0, "du": 0, "dd": 0}
    normalization = 0
    for state in states:
        out[state[0] + state[1]] += states[state] / 2
        out[state[1] + state[2]] += states[state] / 2
        normalization += states[state]

    out = {k: v / normalization for (k, v) in out.items()}


if __name__ == "__main__":
    N = 500000
    grid = Ising1D(N, 0.5)

    correct = []
    grid.loop(10000000)

    states = grid.count_normalized_states()

    grid2 = generate_chain(N, states)
    states2 = grid2.count_normalized_states()

    print("old", states)
    print("new", states2)
