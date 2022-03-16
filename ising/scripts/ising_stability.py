import itertools
import math


def probability_towards_local_stability(pb, T):
    total = 0.0

    towards_stability = 0.0
    towards_chaos = 0.0
    do_nothing = 0.0

    for state in itertools.product([0, 1], repeat=5):
        p = 1
        for c in state:
            if c == 1:
                p *= pb
            if c == 0:
                p *= 1 - pb

        dE = 0
        if state[0] == 0:
            dE = 2 * state[1:].count(0) + -2 * state[1:].count(1)
        if state[0] == 1:
            dE = -2 * state[1:].count(0) + 2 * state[1:].count(1)

        print(str(state[0]), "".join([str(i) for i in state[1:]]), p, dE)
        total += p

        # Towards Black
        if (state[0] == 0 and state[1:].count(0) < 2) or (state[0] == 1 and state[1:].count(1) < 2):
            print("towards stability")
            if dE < 0:
                towards_stability += p
            else:
                towards_stability += p * (math.exp(-dE / T))
                do_nothing += p * (1 - math.exp(-dE / T))

        elif state[1:].count(1) == 2:
            print("do nothing?")
            if dE < 0:
                do_nothing += p
            else:
                do_nothing += p * (math.exp(-dE / T))
        else:
            print("towards chaos")
            if dE < 0:
                towards_chaos += p
            else:
                towards_chaos += p * (math.exp(-dE / T))
                do_nothing += p * (1 - math.exp(-dE / T))

    print("towards stability", towards_stability)
    print('towards chaos', towards_chaos)
    print("do nothing", do_nothing)
    sumy = towards_stability + towards_chaos + do_nothing
    print("sum", sumy)
    assert abs(sumy - 1) < 0.01

    # towards_black_final = towards_black
    # for i in range(1, 2000):
    #   towards_black_final += towards_black * ((do_nothing) ** i)
    towards_stability_final = towards_stability / (1 - do_nothing)

    return towards_stability_final


# probability_towards_local_stability(0.2, 2.3)
# exit(1)

import matplotlib.pyplot as plt
import numpy as np


# Ts = [0.01, 1, 2, 2.269185, 2.5, 3, 4, 5]


# Ts = [2.1, 2.2, 2.3, 2.4]
# Ts = [1.0, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9, 2.0]

Ts = np.arange(1.9, 2.4, 0.05)

pbs = np.arange(0.1, 0.9, 0.1)

for pb in pbs:
    ys = [probability_towards_local_stability(pb, t) for t in Ts]

    plt.plot(Ts, ys, label="pb=" + str(pb))  # plotting t, a separately

    plt.xlabel("Temperature")
    plt.ylabel("Move towards stability")

# plt.xticks()
# plt.xticks(np.arange(0, 1, 0.1))
# plt.yticks(np.arange(0, 1, 0.1))

plt.legend()
plt.grid(True)
plt.show()
# plt.show(block=False)
# plt.pause(10)
# plt.close()


# from scipy.optimize import fsolve
# from functools import partial

# print(
#     fsolve(
#         partial(
#             lambda T, pb: probability_towards_black(pb, T) - 0.5,
#             1.5,
#         ),
#         0.2,
#     )
# )
