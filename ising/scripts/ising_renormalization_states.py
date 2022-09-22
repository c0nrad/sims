from ising import Ising
import matplotlib.pyplot as plot
from ising_state_vector import IsingStateVector
import numpy as np
import math
from typing import Dict
from ising_state_vector import IsingStateVector
from ising import Ising
import numpy as np
import random
import math
import matplotlib.pyplot as plot
from utils import majority, value_to_ud, ud_to_value


def block_grid(model: Ising, a: int):
    blocked = Ising(model.gridSize / a, 0)

    for x in range(blocked.gridSize):
        for y in range(blocked.gridSize):
            original_x = x * a
            original_y = y * a

            block = ""
            for dx in range(a):
                for dy in range(a):
                    block += value_to_ud(model.at(original_x + dx, original_y + dy))
            result = majority(block)

            blocked.set(x, y, ud_to_value(result))

    return blocked


L = 90
block_size = 3
i = Ising(L, 3)
i.loop(10000000)

results = {}
Ts = np.linspace(3, 1.5, 50)
for t in Ts:
    print(t)
    i.T = t

    avg_states = {}
    iterations = 1000
    for _ in range(iterations):
        i.loop(4000 * L * L)

        blocked_i = block_grid(i, block_size)

        v = IsingStateVector(i)
        v.normalize_probabilities()
        blocked_v = IsingStateVector(blocked_i)
        blocked_v.normalize_probabilities()

        for state in v.states:
            # if state[0] != "u":
            #     continue
            if state not in avg_states:
                avg_states[state] = 0
            avg_states[state] += v.states[state]

        for state in blocked_v.states:
            # if state[0] != "u":
            #     continue
            b_state = "b_" + state
            if b_state not in avg_states:
                avg_states[b_state] = 0
            avg_states[b_state] += blocked_v.states[state]

    for state in avg_states:
        if state not in results:
            results[state] = []

        results[state].append(avg_states[state] / iterations)

print(results)
for state in results:
    if (state[0]) == "u":
        continue
    if (state[0]) == "b" and state[2] == "u":
        continue
    plot.plot(Ts, results[state], label=state)
plot.legend()
plot.show()

# {'uuuuu': 0.31860382827454153, 'uuuud': 0.11006524473612249, 'uuudd': 0.033584522832923146, 'uudud': 0.006982608695652079, 'uuddd': 0.019013016133442816, 'udddd': 0.009498878862455491, 'ddddd': 0.32248706590101117, 'ddddu': 0.11092879409351909, 'ddduu': 0.03359819524200149, 'ddudu': 0.006975170905113386, 'dduuu': 0.018892152037189084, 'duuuu': 0.009370522286026702}

# {'uuuuu': 0.31860382827454153, 'uuuud': 0.11006524473612249, 'uuudd': 0.033584522832923146, 'uudud': 0.006982608695652079, 'uuddd': 0.019013016133442816, 'udddd': 0.009498878862455491, 'ddddd': 0.32248706590101117, 'ddddu': 0.11092879409351909, 'ddduu': 0.03359819524200149, 'ddudu': 0.006975170905113386, 'dduuu': 0.018892152037189084, 'duuuu': 0.009370522286026702}

# {'uuuuu': 0.3067076923076923, 'uuuud': 0.11723846153846154, 'uuudd': 0.039023076923076924, 'uudud': 0.007669230769230769, 'uuddd': 0.020484615384615382, 'udddd': 0.008815384615384616, 'ddddd': 0.30504615384615386, 'ddddu': 0.11964615384615383, 'ddduu': 0.03948461538461539, 'ddudu': 0.007546153846153846, 'dduuu': 0.01972307692307692, 'duuuu': 0.008615384615384613}
