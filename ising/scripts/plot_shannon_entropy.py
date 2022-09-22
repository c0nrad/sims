from functools import reduce
import math
from sre_compile import isstring
from builder import ones_grid
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
import matplotlib.pyplot as plot


L = 50
Ts = np.linspace(5, 0.1, 50)
m = Ising(L, 0.1)
entropy = []
energy = []
freeEnergy = []
for t in Ts:
    print(t)
    iterations = 100
    avg_entropy = 0
    avg_energy = 0
    m.T = t
    for i in range(iterations):
        m.loop(5000 * L * L)

        v = IsingStateVector(m)
        avg_entropy += v.calculate_shannon_entropy()
        avg_energy += v.calculate_energy_per_spin()

    entropy.append(avg_entropy / iterations)
    energy.append(avg_energy / iterations)
    freeEnergy.append(avg_energy / iterations - t * avg_entropy / iterations)

plot.plot(Ts, entropy, label="Entropy")
plot.plot(Ts, energy, label="energy")
# plot.plot(Ts, freeEnergy, label="Free Energy")
plot.legend()
plot.show()
