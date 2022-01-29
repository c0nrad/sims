import itertools
import math


def probability_towards_black(pb, T):
    total = 0.0

    towards_black = 0
    towards_white = 0
    do_nothing = 0

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

        # print(str(state[0]), "".join([str(i) for i in state[1:]]), p, dE)
        total += p

        # Towards Black
        if state[0] == 0:
            if dE < 0:
                towards_black += p
            else:
                towards_black += p * (math.exp(-dE / T))

        # Do nothing
        if dE >= 0:
            do_nothing += p * (1 - math.exp(-dE / T))
            # towards_black += p * (1 - math.exp(-dE / T))

        # Towards White
        if state[0] == 1:
            if dE < 0:
                towards_white += p
            else:
                towards_white += p * (math.exp(-dE / T))

    # print("total", total)
    # print("towards black", towards_black)
    # print('towards white', towards_white)
    # print("do nothing", do_nothing)
    # print("sum", towards_white + towards_black + do_nothing)

    towards_black_final = towards_black
    for i in range(1, 200000):
        towards_black_final += towards_black * ((do_nothing) ** i)

    print(f'pb={pb :.2f} T={T:.2f}, TowardsBlack={towards_black_final:.3f}')

    return towards_black_final


import matplotlib.pyplot as plt
import numpy as np

# Ts = [0.01, 1, 2, 2.269185, 2.5, 3, 4, 5]
# Ts = [2.1, 2.2, 2.3, 2.4]
# Ts = [1.0, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9, 2.0]

Ts = np.arange(1.9, 2.4, 0.05)

pbs = np.arange(0.01, 0.5, 0.01)

for t in Ts:
    ys = [probability_towards_black(pb, t) for pb in pbs]

    plt.plot(pbs, ys, label="T=" + str(t))  # plotting t, a separately

    plt.xlabel("Probability of Black")
    plt.ylabel("Move towards Black")

# plt.xticks()
plt.xticks(np.arange(0, 1, 0.1))
plt.yticks(np.arange(0, 1, 0.1))

plt.legend()
plt.grid(True)
plt.show()

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
