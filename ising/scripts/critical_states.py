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

avg_states = {}
hits = 0
# Tc = 2 / math.log(math.sqrt(2) + 1)
L = 20

i = Ising(L, 0)

results = {}
Ts = np.linspace(5, 0.1, 20)
for t in Ts:
    print(t)
    i.T = t

    avg_states = {}
    iterations = 10
    for _ in range(iterations):
        print(avg_states)
        i.loop(20 * L * L)
        m = i.calculateMagnatism()

        v = IsingStateVector(i)
        v.normalize_probabilities()

        for state in v.states:
            if state not in avg_states:
                avg_states[state] = 0
            avg_states[state] += v.states[state]

    for state in avg_states:
        if state not in results:
            results[state] = []

        results[state].append(avg_states[state] / iterations)

print(results)
for state in results:
    plot.plot(Ts, results[state], label=state)
plot.show()

# {'uuuuu': 0.31860382827454153, 'uuuud': 0.11006524473612249, 'uuudd': 0.033584522832923146, 'uudud': 0.006982608695652079, 'uuddd': 0.019013016133442816, 'udddd': 0.009498878862455491, 'ddddd': 0.32248706590101117, 'ddddu': 0.11092879409351909, 'ddduu': 0.03359819524200149, 'ddudu': 0.006975170905113386, 'dduuu': 0.018892152037189084, 'duuuu': 0.009370522286026702}

# {'uuuuu': 0.31860382827454153, 'uuuud': 0.11006524473612249, 'uuudd': 0.033584522832923146, 'uudud': 0.006982608695652079, 'uuddd': 0.019013016133442816, 'udddd': 0.009498878862455491, 'ddddd': 0.32248706590101117, 'ddddu': 0.11092879409351909, 'ddduu': 0.03359819524200149, 'ddudu': 0.006975170905113386, 'dduuu': 0.018892152037189084, 'duuuu': 0.009370522286026702}

# {'uuuuu': 0.3067076923076923, 'uuuud': 0.11723846153846154, 'uuudd': 0.039023076923076924, 'uudud': 0.007669230769230769, 'uuddd': 0.020484615384615382, 'udddd': 0.008815384615384616, 'ddddd': 0.30504615384615386, 'ddddu': 0.11964615384615383, 'ddduu': 0.03948461538461539, 'ddudu': 0.007546153846153846, 'dduuu': 0.01972307692307692, 'duuuu': 0.008615384615384613}
