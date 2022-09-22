from ising import Ising
from ising_state_vector import IsingStateVector
import numpy as np
import math


def single_cell_vector(N):
    i2 = Ising(N, 1)
    i2.grid = np.ones((N, N), dtype=np.int64)
    i2.grid[0][0] = -1
    # i2.grid[2][2] = -1

    return IsingStateVector(i2)


def empty_grid(L):
    return np.zeros((L, L))


def diamond(L):
    grid = np.asarray(
        [
            [-1, -1, 1, -1, -1],
            [-1, 1, 1, 1, -1],
            [1, 1, 1, 1, 1],
            [-1, 1, 1, 1, -1],
            [-1, -1, 1, -1, -1],
        ]
    )

    # for x in range(-L // 2, L // 2):
    #     for y in range(-L // 2, L // 2):
    #         if abs(x) + abs(y) < (L + 1) // 2:
    #             grid[x % L][y % L] = int(-1)

    return grid
