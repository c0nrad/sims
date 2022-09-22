from ising_state_solution import probability_to_next_states, weighted_avg_and_std
from typing import Dict
from ising_state_vector import IsingStateVector
from ising import Ising
import numpy as np
import random
import math
import matplotlib.pyplot as plot


print("Critical T", 2 / math.log(1 + math.sqrt(2)))

gridSize = 50
original_model = Ising(gridSize, 20)
print("GridSize = ", gridSize, "Temp =", original_model.T)
original_model.loop(1000000)
# original_model.dump()
original_vector = IsingStateVector(original_model)
print(original_vector.states)
print("original mag", original_model.calculateMagnatism())
original_mag = original_vector.calculate_magnetism()

M_mean = []
M_std = []
Ts = np.linspace(1, 5, 10)
for t in Ts:
    print(t)

    # 2.26918531421
    next_vector = probability_to_next_states(original_vector, t)
    next_vector = dict(sorted(next_vector.items(), key=lambda item: item[1], reverse=True))

    mean, std = weighted_avg_and_std([v.calculate_magnetism() for v in next_vector], list(next_vector.values()))

    M_mean.append(mean)
    M_std.append((std) / t)

# M_std = np.asarray(M_std)
# M_std

# plot.plot(Ts, Ms)
plot.plot(Ts, M_mean)
# plot.plot(Ts, Cs_old)
plot.legend()

plot.grid()
plot.show()
plot.pause(0)
