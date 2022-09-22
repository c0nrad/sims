import math
import random
import numpy as np
from numba import int64, float64, int8
from numba.experimental import jitclass
import colorama
from scipy.optimize import curve_fit
from copy import copy, deepcopy
import matplotlib.pyplot as plot

from ising_1d import Ising

import time

gridS = 1000


def entropy_solution(t):
    return math.log(2) / gridS + (-(1 / t) * math.tanh(1 / t) + math.log(2 * math.cosh(1 / t)))


model = Ising(gridS, 2)

Ts = np.linspace(5, 0.1, 50)

steps = 500000

entropy = []

for t in Ts:
    print(t)
    model.T = t

    iterations = 20

    avg_entropy = 0
    for _ in range(iterations):
        model.loop(steps)

        avg_entropy += model.calculateEntropy()
        # Break symmetry
        # if states["uuu"] < states["ddd"]:
        #     states["uuu"], states["ddd"] = states["ddd"], states["uuu"]
        #     states["uud"], states["ddu"] = states["ddu"], states["uud"]
        #     states["udd"], states["duu"] = states["duu"], states["udd"]
        #     states["udu"], states["dud"] = states["dud"], states["udu"]

    entropy.append(avg_entropy / iterations)

print(entropy)

plot.plot(Ts, entropy, label="Entropy")
plot.plot(Ts, [entropy_solution(t) for t in Ts], label="Solution")
plot.legend(loc="upper right")


plot.show()
