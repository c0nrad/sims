import itertools
import math



def probability_towards_black(pb, T):
    pb = 

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
            if dE <= 0:
                towards_black += p
            else:
                towards_black += p * (math.exp(-dE / T))

        # Do nothing
        if dE > 0:
            do_nothing += p * (1 - math.exp(-dE / T))
            # towards_black += p * (1 - math.exp(-dE / T))

        # Towards White
        if state[0] == 1:
            if dE <= 0:
                towards_white += p
            else:
                towards_white += p * (math.exp(-dE / T))

    # print("total", total)
    # print("towards black", towards_black)
    # print('towards white', towards_white)
    # print("do nothing", do_nothing)
    print("sum", towards_white + towards_black + do_nothing)

    if abs(towards_white + towards_black + do_nothing - 1) > 0.01:
        print("bad sum")
        exit(1)

    # towards_black_final = towards_black
    # for i in range(1, 2000):
    #   towards_black_final += towards_black * ((do_nothing) ** i)
    towards_black_final = towards_black / (1 - do_nothing)

    print(f'pb={pb :.2f} T={T:.2f}, TowardsBlack={towards_black_final:.3f}')

    return towards_black_final


import matplotlib.pyplot as plt
import numpy as np

maxy = 1

T = 2.24
for pb in np.arange(0.01, 0.51, 0.01):
    b = probability_towards_black(pb, T)
    assert b < maxy, "b should be less" + str(b - maxy)
    maxy = b

print("no upward")
# [probability_towards_black(pb, t) - 0.5 for pb in pbs]


exit(0)


# Ts = [0.01, 1, 2, 2.269185, 2.5, 3, 4, 5]
# Ts = [2.1, 2.2, 2.3, 2.4]
# Ts = [1.0, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9, 2.0]

Ts = np.arange(1.9, 2.4, 0.05)

pbs = np.arange(0.01, 0.51, 0.01)

for t in Ts:
    ys = [probability_towards_black(pb, t) - 0.5 for pb in pbs]

    plt.plot(pbs, ys, label="T=" + str(t))  # plotting t, a separately

    plt.xlabel("Probability of Black")
    plt.ylabel("Move towards Black")

# plt.xticks()
plt.xticks(np.arange(0, 1, 0.1))
plt.yticks(np.arange(0, 1, 0.1))

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
