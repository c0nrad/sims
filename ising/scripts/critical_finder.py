from typing import Dict
from ising_state_solution import probability_to_next_states
from ising_state_vector import IsingStateVector
from ising import Ising
import numpy as np
import random
import math
import matplotlib.pyplot as plot
import grid_builder


def estimate_critical_temperature():
    print("Critical T", 2 / math.log(1 + math.sqrt(2)))

    gridSize = 10

    original_model = Ising(gridSize, 1)
    # for x in range(gridSize):
    #     for y in range(gridSize):
    #         if y < gridSize / 2:
    #             original_model.grid[x][y] = 1
    #         else:
    #             original_model.grid[x][y] = -1

    print("GridSize = ", gridSize, "Temp =", original_model.T)
    # original_model.loop(1000000000)
    original_vector = IsingStateVector(original_model)
    print(original_vector.states)
    print("original mag", original_model.calculateMagnatism())
    (C1_original, C2_original) = original_vector.calculate_simple_correlation_function()
    print("original dist function", original_vector.calculate_simple_correlation_function())

    while True:
        t_guess = 2

        # 2.26918531421
        next_vector = probability_to_next_states(original_vector, t_guess)
        next_vector = dict(sorted(next_vector.items(), key=lambda item: item[1], reverse=True))

        max_c1, max_t = 0, 0
        for (vector, p) in list(next_vector.items()):
            C1_avg += (vector.calculate_simple_correlation_function()[0]) * p
            C2_avg += (vector.calculate_simple_correlation_function()[1]) * p
            print(p, vector)

        # c_avg_old += vector.calculate_correlation_distance(2) * p
        # print("original_mag", original_mag, "new mag", dM)
        # print("original_c", original_C, "new c", c_avg)
        # print("original_c", original_C, "new_c", c_avg)
        # print("long c", c_avg_old)
        C1.append(C1_avg)
        C2.append(C2_avg)

        print("Recent C1, C2", C1[-1], C2[-1])

        # print("down, up", down, up)
        # Cs.append(avg)
        # print("result", t, Cs[-1])

    plot.plot(Ts, C1, label="c1")
    # plot.plot(Ts, C2, label="c2")

    plot.axhline(C1_original)
    # plot.axhline(C2_original)
    plot.legend()

    plot.grid()
    plot.show()
    plot.pause(0)
