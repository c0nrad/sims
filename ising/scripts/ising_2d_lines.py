import numpy as np
import matplotlib.pyplot as plot
from ising import Ising
from ising_state_vector import IsingStateVector

from ising_1d_chains import get_next_spin_probabilistic

N = 200
grid = Ising(N, 1)
count_uuu = []
p_uuu = []
count_uud = []
p_uud = []
count_dud = []
p_dud = []
count_uuuu = []
p_uuuu = []

count_uuduu = []
p_uuduu = []

Ts = np.linspace(8, 0.1, 20)
for t in Ts:
    print(t)
    grid.T = t

    average_count_uuu = 0
    average_p_uuu = 0

    average_count_uud = 0
    average_p_uud = 0

    average_count_dud = 0
    average_p_dud = 0

    average_count_uuuu = 0
    average_p_uuuu = 0

    average_count_uuduu = 0
    average_p_uuduu = 0

    iters = 30
    for i in range(iters):
        grid.loop(100000)

        states = IsingStateVector(grid).states
        # states = states.states

        count = 0
        for row in range(N):
            for i in range(N):
                # if grid.at(row, i) == 1 and grid.at(row, i + 1) == 1 and grid.at(row, i + 2) == 1:
                #     average_count_uuu += 1

                # if grid.at(row, i) == 1 and grid.at(row, i + 1) == 1 and grid.at(row, i + 2) == -1:
                #     average_count_uud += 1

                # if grid.at(row, i) == -1 and grid.at(row, i + 1) == 1 and grid.at(row, i + 2) == 1:
                #     average_count_uud += 1

                # if grid.at(row, i) == -1 and grid.at(row, i + 1) == 1 and grid.at(row, i + 2) == -1:
                #     average_count_dud += 1

                # if (
                #     grid.at(row, i) == 1
                #     and grid.at(row, i + 1) == 1
                #     and grid.at(row, i + 2) == 1
                #     and grid.at(row, i + 3) == 1
                #     # and grid.at(row, i + 4) == 1
                # ):
                #     average_count_uuuu += 1

                if (
                    grid.at(row, i) == 1
                    and grid.at(row, i + 1) == 1
                    and grid.at(row, i + 2) == -1
                    and grid.at(row, i + 3) == 1
                    and grid.at(row, i + 4) == 1
                ):
                    average_count_uuduu += 1

        # print("Four Up Count", fiveUpCount)
        # print(states["uuu"] * states["uuu"] / (states["uud"] / 2 + states["uuu"]) * N)

        # print(sum(states.values()))

        p_uuu_curr = states["uuuuu"] + states["uuuud"] / 2 + states["uudud"] / 2
        p_uud_curr = 2 * ((states["uuuud"] / 4) + (states["uuudd"] / 2) + (states["uuddd"] / 4))
        p_dud_curr = states["udddd"] + states["uuddd"] / 2 + states["uudud"] / 2

        p_ddd_curr = states["ddddd"] + states["ddddu"] / 2 + states["ddudu"] / 2
        p_ddu_curr = 2 * ((states["ddddu"] / 4) + (states["ddduu"] / 2) + (states["dduuu"] / 4))
        p_udu_curr = states["duuuu"] + states["dduuu"] / 2 + states["ddudu"] / 2

        # p_uuu_curr =

        # print(p_uuu + 2 * p_uud + p_dud)

        # p_uuuu = p_uuu * (p_uuu) / (p_uuu + p_uud)

        # line_b = states[""]
        # print("Equal?", fiveUpCount, p_uuu * (p_uuu / (p_uuu + (2 * p_uud) + p_dud)))

        p_u_given_uu = 0
        if p_uuu_curr != 0:
            p_u_given_uu = p_uuu_curr / (p_uuu_curr + p_uud_curr / 2)

        p_u_given_ud = 0
        if p_udu_curr != 0:
            p_u_given_ud = p_udu_curr / (p_ddu_curr / 2 + p_udu_curr)

        p_u_given_du = 0
        if p_uud_curr != 0:
            p_u_given_du = p_uud_curr / 2 / (p_uud_curr / 2 + p_dud_curr)

        # average_p_uuu += p_uuu_curr
        # average_p_uud += p_uud_curr
        # average_p_dud += p_dud_curr
        average_p_uuduu += (p_uud_curr / 2) * p_u_given_ud * p_u_given_du

        # print(average_p_uuduu, p_u_given_ud, p_u_given_du)

        average_p_uuuu += p_uuu_curr * p_u_given_uu

    # p_uuu.append(average_p_uuu / iters)
    # p_uud.append(average_p_uud / iters)
    # p_dud.append(average_p_dud / iters)
    # p_uuuu.append(average_p_uuuu / iters)
    p_uuduu.append(average_p_uuduu / iters)

    # count_uuu.append(average_count_uuu / iters)
    # count_uud.append(average_count_uud / iters)
    # count_dud.append(average_count_dud / iters)
    # count_uuuu.append(average_count_uuuu / iters)
    count_uuduu.append(average_count_uuduu / iters)

# plot.plot(Ts, p_uuu, label="p_uuu")
# plot.plot(Ts, p_uud, label="p_uud")
# plot.plot(Ts, p_dud, label="p_dud")
plot.plot(Ts, p_uuduu, label="p_uuduu")

# plot.plot(Ts, count_uuu, label="count_uuu")
# plot.plot(Ts, count_uud, label="count_uud")
# plot.plot(Ts, count_dud, label="count_dud")
plot.plot(Ts, count_uuduu, label="count_uuduu")


plot.legend()
plot.show()
plot.pause(0)
