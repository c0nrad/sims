from typing import Dict
from builder import string_rotate
from ising_state_vector import IsingStateVector
from ising import Ising
import numpy as np
import random
import math
import matplotlib.pyplot as plot
import grid_builder


# test_i = Ising(7, 1)
# test_i.grid = np.ones((7, 7), dtype=np.int64)
# test_i.grid[0][0] = -1
# test_vector = IsingStateVector(test_i)


def generate_probability_of_occurance_map(vector: IsingStateVector, N):
    # Given some ordered states such as "ud000" or "ud0d0", what is their probability of occuring?

    out = {
        "00000": 0,
        "u0000": 0,
        "d0000": 0,
        "uu000": 0,
        "ud000": 0,
        "du000": 0,
        "dd000": 0,
        "uu0u0": 0,
        "uu0d0": 0,
        "ud0u0": 0,
        "ud0d0": 0,
        "du0u0": 0,
        "du0d0": 0,
        "dd0u0": 0,
        "dd0d0": 0,
        # "uuu00": 0,
        # "uud00": 0,
        # "udu00": 0,
        # "udd00": 0,
        # "duu00": 0,
        # "dud00": 0,
        # "ddu00": 0,
        # "ddd00": 0,
        "uuuu0": 0,
        "uuud0": 0,
        "uudu0": 0,
        "uudd0": 0,
        "uduu0": 0,
        "udud0": 0,
        "uddu0": 0,
        "uddd0": 0,
        "duuu0": 0,
        "duud0": 0,
        "dudu0": 0,
        "dudd0": 0,
        "dduu0": 0,
        "ddud0": 0,
        "dddu0": 0,
        "dddd0": 0,
    }
    total_states = vector.total_states()
    for (state, p) in vector.states.items():
        # Single Corner
        out["00000"] = 1

        corners = state[1:]
        for c in range(4):
            out[state[0] + "0000"] += p / total_states / 4
            out[state[0] + corners[c] + "000"] += p / total_states / 4.0
            out[state[0] + corners[c] + "0" + corners[(c + 2) % 4] + "0"] += p / total_states / 4.0
            # out[state[0] + corners[c] + corners[(c + 1) % 4] + "00"] += p / total_states / 4.0
            out[state[0] + corners[c] + corners[(c + 1) % 4] + corners[(c + 2) % 4] + "0"] += p / total_states / 4.0
            # out[state[0] + corners[c] + corners[(c + 1) % 4] + corners[(c + 2) % 4] + corners[(c + 3) % 4]] += (
            # p / total_states / 4.0
            # )

    return out


# assert generate_probability_of_occurance_map(test_vector, 7)[""]


def count_fit(state_constrains: str, vector: IsingStateVector):
    fits = 0

    if state_constrains == "00000":
        return sum([1 for (a, p) in vector.states.items() if p != 0])

    if state_constrains.count("0") == 0:
        return vector.states[state_constrains]

    for (state, p) in vector.states.items():
        if p == 0:
            continue

        if state[0] != state_constrains[0] and state_constrains[0] != "0":
            continue

        corners = state[1:]
        known_corners = set()
        for i in range(4):

            is_match = True
            for s in range(4):
                if state_constrains[s + 1] != "0" and state_constrains[s + 1] != corners[(s + 1 + i) % 4]:
                    is_match = False
                    break

            if is_match and string_rotate(corners, i + 1) not in known_corners:
                fits += 1
                known_corners.add(string_rotate(corners, i + 1))
        # print(known_corners)

    return fits


def count_unique_fits(state_constrains: str, vector: IsingStateVector):
    if len(state_constrains) != 5:
        raise Exception("invalud length")

    fits = 0

    if state_constrains == "00000":
        return sum([1 for (a, p) in vector.states.items() if p != 0])

    # if state_constrains.count("0") == 0:
    #     return vector.states[state_constrains]

    for (state, p) in vector.states.items():
        if p == 0:
            continue

        if state[0] != state_constrains[0] and state_constrains[0] != "0":
            continue

        corners = state[1:]
        known_corners = set()
        for i in range(4):

            is_match = True
            for s in range(4):
                if state_constrains[s + 1] != "0" and state_constrains[s + 1] != corners[(s + 1 + i) % 4]:
                    is_match = False
                    break

            if is_match:
                fits += p / 4

        # print(known_corners)

    return fits


# 2 c + 2 d + b E^(-4/t) + 3 e E^(4/t) + 4 E^(8/t) f
# assert count_fit("00000", grid_builder.single_cell_vector(4)) == 16
# assert count_fit("uu000", grid_builder.single_cell_vector(4)) == 15
# assert count_fit("ud000", grid_builder.single_cell_vector(4)) == 4
# assert count_fit("du000", grid_builder.single_cell_vector(4)) == 1

# assert count_fit("00000", grid_builder.single_cell_vector(5)) == 16
# assert count_fit("uu000", grid_builder.single_cell_vector(5)) == 15
# assert count_fit("ud000", grid_builder.single_cell_vector(5)) == 4
# assert count_fit("du000", grid_builder.single_cell_vector(5)) == 1


def count_constraints(N):
    out = [1, 0, N - 3, 2, (N - 3) * N, 2 * N]
    return out


assert count_constraints(7) == [1, 0, 4, 2, 28, 14]

# print(count_constraints(6))


def calculate_probabilisitc_multiplicity(vector, N):
    # How many ways can I construct a board with the given vector

    constraint_counts = count_constraints(N)
    probability_of_occurance = generate_probability_of_occurance_map(vector, N)

    print(f"constraint_count={constraint_counts}")
    print(f"probability_of_occurance={probability_of_occurance}")
    # count_of_fits = generate_count_of_fits_map(vector, N)

    # g = 1
    g = 0

    constraint_multiplicity = [0, 0, 0, 0, 0, 0]
    for (state, p) in probability_of_occurance.items():
        # print("Constrains_multiplicity", state, p, count_fit(state, vector))
        constraint_multiplicity[5 - state.count("0")] += p * count_unique_fits(state, vector)

        print(f"constraint_multiplicity state={state}, p={p}, count_fit={count_unique_fits(state, vector)}")

    # print(f'Constrains_Multpilicity={constraint_multiplicity}')
    for i in range(5):
        if constraint_counts[i] == 0:
            continue
        print(
            f"i={i} constraint_counts[i]={constraint_counts[i]}, constraint_multiplicity[i]={constraint_multiplicity[i]}"
        )

        # How many squares have 1,2,3,4,5 constraints times the "fit" for those squares
        # g *= pow(constraint_multiplicity[i], constraint_counts[i])
        g += constraint_multiplicity[i] * constraint_counts[i]

    print(f"g={g}")
    # Remove duplicates
    # for (state, p) in vector.states.items():
    #     g /= math.factorial(p)

    # How many symmetries?
    # Up Down Left Right Rotate 90 rotate

    return g
    # return g / 6 / (N ** 2)


def calculate_constraint_map(L):
    constraints = {}

    grid = np.zeros((L, L), dtype=np.int64)
    for x in range(L):
        for y in range(L):
            k = (
                str(grid[x][y])
                + str(grid[x][(y - 1) % L])
                + str(grid[(x + 1) % L][y])
                + str(grid[x][(y + 1) % L])
                + str(grid[(x - 1) % L][y])
            )
            print(k)
            print(str(grid[x][y]))
            print(str(grid[x][(y - 1) % L]))

            grid[x][y] = 1
            grid[x][(y - 1) % L] = 1
            grid[(x + 1) % L][y] = 1
            grid[x][(y + 1) % L] = 1
            grid[(x - 1) % L][y] = 1

            if k in constraints:
                constraints[k] += 1
            else:
                constraints[k] = 1

    return constraints


# N = 5
# i = Ising(N, 1)
# i.grid = np.ones((N, N), dtype=np.int64)
# i.grid[0][0] = -1
# # i.grid[3][3] = -1

# vector = IsingStateVector(i)
# print("N=", N)
# print("vector.states", vector.states)

# print(calculate_probabilisitc_multiplicity(vector, N))


N = 20
i2 = Ising(N, 1)
i2.grid = np.ones((N, N), dtype=np.int64)
i2.grid[0][0] = -1
i2.grid[2][2] = -1
# i2.grid[4][4] = -1


vector2 = IsingStateVector(i2)
print("N=", N)
print("vector.states", vector2.states)

print(calculate_probabilisitc_multiplicity(vector2, N))
