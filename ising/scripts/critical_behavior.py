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


C_old = []
C_new = []
Ts = np.linspace(1, 5, 21)
for t in Ts:
    print(t)

    i = Ising(100, t)
    i.loop(100000000)

    v = IsingStateVector(i)

    c_old = v.calculate_correlation_distance(6)
    # print(v.calculate_correlation_function(3))
    c_new = v.calculate_simple_correlation_distance()
    # print(c_old, c_new)
    C_old.append(c_old)
    C_new.append(c_new)


plot.plot(Ts, C_old, label="c_old")
plot.plot(Ts, C_new, label="c_new")
plot.legend()
plot.show()
plot.pause(0)
