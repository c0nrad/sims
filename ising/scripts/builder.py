import re
from typing import Dict
from ising_state_vector import IsingStateVector
from utils import ud_to_value, value_to_ud
from ising import Ising
import numpy as np
import random
import math
import matplotlib.pyplot as plot
import grid_builder
import sympy


def string_rotate(s, i):
    while i != 0:
        s = s[1:] + s[0]
        i -= 1
    return s


assert string_rotate("abcd", 1) == "bcda"
assert string_rotate("abcd", 0) == "abcd"
assert string_rotate("abcd", 4) == "abcd"


def get_state_probabilities_from_requirements(vector, requirements):
    possible_states = {}
    for (state, p) in vector.states.items():
        if p == 0:
            continue

        if state[0] != requirements[0] and requirements[0] != "0":
            continue

        corners = state[1:]
        for i in range(4):

            is_match = True
            for s in range(4):
                if requirements[s + 1] == "0":
                    continue

                if requirements[s + 1] != corners[(s + 1 + i) % 4]:
                    is_match = False
                    break

            if is_match:
                if state[0] + string_rotate(corners, i + 1) not in possible_states:
                    possible_states[state[0] + string_rotate(corners, i + 1)] = 0

                possible_states[state[0] + string_rotate(corners, i + 1)] += p / 4

    total_p = sum(possible_states.values())
    return {s: p / total_p for (s, p) in possible_states.items()}


assert get_state_probabilities_from_requirements(
    IsingStateVector.from_states({"uuuuu": 0.5, "uuudd": 0.5}), "uuu00"
) == {
    'uuuuu': 0.8,
    'uuudd': 0.2,
}

assert get_state_probabilities_from_requirements(
    IsingStateVector.from_states({"uuuuu": 0.5, "uuudd": 0.5}), "uuuu0"
) == {
    'uuuuu': 1,
}

assert get_state_probabilities_from_requirements(
    IsingStateVector.from_states({"uuuuu": 0.5, "uuudd": 0.5}), "uu000"
) == {
    'uuuuu': 4 / 6,
    'uuudd': 1 / 6,
    "uuddu": 1 / 6,
}
# assert len(get_state_probabilities_from_requirements(grid_builder.single_cell_vector(4), "u0000")) == 60
# assert len(get_state_probabilities_from_requirements(grid_builder.single_cell_vector(4), "d0000")) == 4
# assert len(get_state_probabilities_from_requirements(grid_builder.single_cell_vector(4), "du000")) == 4
# assert len(get_state_probabilities_from_requirements(grid_builder.single_cell_vector(4), "duuuu")) == 4
# assert len(get_state_probabilities_from_requirements(grid_builder.single_cell_vector(4), "duduu")) == 0
# assert len(get_state_probabilities_from_requirements(grid_builder.single_cell_vector(4), "00000")) == 64


def generate_board_from_vector_probabilistic(vector, N):

    model = Ising(N, 0)
    model.grid = np.zeros((N, N))

    requirements = "00000"
    coords = []
    for x in range(N):
        for y in range(N):

            requirements = (
                model.at(x, y),
                model.at(x, y - 1),
                model.at(x + 1, y),
                model.at(x, y + 1),
                model.at(x - 1, y),
            )

            requirements = "".join([value_to_ud(a) for a in requirements])
            possible_states = get_state_probabilities_from_requirements(vector, requirements)

            if len(possible_states) == 0:
                print("Could not fit", requirements)
                return

            new_state = np.random.choice(list(possible_states.keys()), p=list(possible_states.values()))

            # print(x, y, requirements, new_state)
            print(x, y, requirements, possible_states, new_state)

            model.set(x, y, ud_to_value(new_state[0]))
            model.set(x, y - 1, ud_to_value(new_state[1]))
            model.set(x + 1, y, ud_to_value(new_state[2]))
            model.set(x, y + 1, ud_to_value(new_state[3]))
            model.set(x - 1, y, ud_to_value(new_state[4]))

        model.dump()

    # model.dump()
    print()
    return model


def generate_board_from_vector_probabilistic_sprinkle(vector, N):

    model = Ising(N, 0)
    model.grid = np.zeros((N, N))

    sampled_states = {}

    requirements = "00000"
    coords = []
    for x in range(N):
        for y in range(N):
            coords.append((x, y))
    random.shuffle(coords)
    for (x, y) in coords:

        new_state = np.random.choice(list(vector.states.keys()), p=list(vector.states.values()))

        if new_state not in sampled_states:
            sampled_states[new_state] = 0
        sampled_states[new_state] += 1

        # print(x, y, requirements, new_state)
        # print(x, y, new_state)

        model.set(x, y, ud_to_value(new_state[0]))
        model.set(x, y - 1, ud_to_value(new_state[1]))
        model.set(x + 1, y, ud_to_value(new_state[2]))
        model.set(x, y + 1, ud_to_value(new_state[3]))
        model.set(x - 1, y, ud_to_value(new_state[4]))

        # model.dump()

    # model.dump()
    print(sampled_states)
    print()
    return model


def generate_board_from_vector_probabilistic_fitted(vector, N):

    model = Ising(N, 0)
    model.grid = np.zeros((N, N))

    x_offset = 0
    y_offset = 0
    while x_offset < N:
        for i in range(N // 2):
            y = (i * 2 + y_offset) % N
            x = (i + x_offset) % N

            new_state = np.random.choice(list(vector.states.keys()), p=list(vector.states.values()))

            # print(x, y, requirements, new_state)
            print(x, y, new_state)

            model.set(x, y, ud_to_value(new_state[0]))
            model.set(x, y - 1, ud_to_value(new_state[1]))
            model.set(x + 1, y, ud_to_value(new_state[2]))
            model.set(x, y + 1, ud_to_value(new_state[3]))
            model.set(x - 1, y, ud_to_value(new_state[4]))

            model.dump()

        if y_offset == -1:
            y_offset = 0
            x_offset += 3
        else:
            y_offset = -1
            x_offset += 2

    # model.dump()
    print()
    return model


def generate_all_boards_from_vector(vector: IsingStateVector, N):
    model = Ising(N, 0)
    model.grid = np.zeros((N, N))

    model.dump()

    queue = [(model, vector)]

    for y in range(N):
        for x in range(N):
            print(x, y, len(queue))

            new_queue = []
            for (model, vector) in queue:
                requirements = (
                    model.at(x, y),
                    model.at(x, y - 1),
                    model.at(x + 1, y),
                    model.at(x, y + 1),
                    model.at(x - 1, y),
                )

                requirements = "".join([value_to_ud(a) for a in requirements])
                possible_states = get_state_probabilities_from_requirements(vector, requirements)

                if len(possible_states) == 0:
                    # print("No valid states", requirements)
                    continue

                possible_states = set(possible_states)
                for new_state in possible_states:
                    new_model = model.clone()
                    new_vector = vector.clone()
                    new_model.set(x, y, ud_to_value(new_state[0]))
                    new_model.set(x, y - 1, ud_to_value(new_state[1]))
                    new_model.set(x + 1, y, ud_to_value(new_state[2]))
                    new_model.set(x, y + 1, ud_to_value(new_state[3]))
                    new_model.set(x - 1, y, ud_to_value(new_state[4]))

                    new_vector.states[new_vector.normalize_state(new_state)] -= 1

                    new_queue.append((new_model, new_vector))

                    # new_model.dump()
                    # print(new_vector.states)
                    # input()

            # Remove duplicates and add to queue
            # print(len(queue), len(new_queue))
            queue = []
            known_lines = set()

            for (model, vector) in new_queue:

                new_line = model.to_line()
                if new_line in known_lines:
                    continue
                else:
                    known_lines.add(new_line)
                    queue.append((model, vector))

    return [model for (model, vector) in queue]


def sympy_vector():
    before = IsingStateVector(None)
    before.states = {
        "uuuuu": sympy.symbols('a', real=True, positive=True, nonzero=True),
        "uuuud": sympy.symbols('b', real=True, positive=True, nonzero=True),
        "uuudd": sympy.symbols('c', real=True, positive=True, nonzero=True),
        "uudud": sympy.symbols('d', real=True, positive=True, nonzero=True),
        "uuddd": sympy.symbols('e', real=True, positive=True, nonzero=True),
        "udddd": sympy.symbols('f', real=True, positive=True, nonzero=True),
        "ddddd": sympy.symbols('g', real=True, positive=True, nonzero=True),
        "ddddu": sympy.symbols('h', real=True, positive=True, nonzero=True),
        "ddduu": sympy.symbols('i', real=True, positive=True, nonzero=True),
        "ddudu": sympy.symbols('j', real=True, positive=True, nonzero=True),
        "dduuu": sympy.symbols('k', real=True, positive=True, nonzero=True),
        "duuuu": sympy.symbols('l', real=True, positive=True, nonzero=True),
    }
    return before


def ones_grid(N):
    i2 = Ising(N, 1)
    i2.grid = np.ones((N, N), dtype=np.int64)
    return i2


if __name__ == "__main__":
    N = 5
    i2 = Ising(N, 1)
    i2.grid = np.ones((N, N), dtype=np.int64)
    i2.grid[0][0] = -1
    i2.grid[2][2] = -1

    vector2 = IsingStateVector(i2)

    # for x in range(50):
    #     generate_board_from_vector_probabilistic(vector2, N)
    #     # input()

    boards = generate_all_boards_from_vector(vector2, N)
    print(f'Len = {len(boards)}')
    for b in boards:
        b.dump()
        print()
    print(f'Len = {len(boards)}')
