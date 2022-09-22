from copy import copy
import itertools
from locale import atoi
import math

from ising_1d import Ising1D
import matplotlib.pyplot as plot


Ls = [5, 6, 7, 8]
counts = []


def sort_key(a):
    return a[0:7] + a[8:][::-1]


def energy(label: str) -> int:
    counts = [int(a) for a in label[0:-1].split(",")]

    # print(counts)
    return counts[0] - counts[2] + counts[3] - counts[5]
    # return counts[0] - counts[2]


def nChooseK(n, k):
    return math.factorial(n) / (math.factorial(k) * math.factorial(n - k))


def guess_multiplicity(N: int, label: str) -> int:
    counts = [int(a) for a in label[0:-1].split(",")]
    labels = ["uuu", "uud", "dud", "ddd", "ddu", "udu"]
    state = {labels[i]: counts[i] for i in range(len(labels))}

    groups = int((1 / 2) * state["uud"] + state["dud"])
    land = N

    print("groups", groups, "land", land)

    if groups == 0:
        return 1

    product = 1
    for i in range(groups):
        product *= land - 3 * i

    return product // groups
    # return int(nChooseK(land, groups))


assert guess_multiplicity(5, "5,0,0,0,0,0,") == 1
assert guess_multiplicity(8, "5,2,0,0,0,1,") == 8
assert guess_multiplicity(5, "1,2,0,0,2,0,") == 5
assert guess_multiplicity(5, "0,2,1,0,0,2,") == 5
assert guess_multiplicity(5, "0,2,0,1,2,0,") == 5
assert guess_multiplicity(5, "0,2,0,1,2,0,") == 5
assert guess_multiplicity(6, "1,2,1,0,0,2,") == 6

# exit(1)/


for L in Ls:
    # L = 11
    grid = Ising1D(L, 0)

    state_counts = {}

    def get_state_key(state) -> str:
        labels = ["uuu", "uud", "dud", "ddd", "ddu", "udu"]
        out = ""
        # return (
        #     str(state["uuu"] + state["ddd"])
        #     + ","
        #     + str(state["uud"] + state["ddu"])
        #     + ","
        #     + str(state["dud"] + state["udu"])
        # )

        if state["ddu"] - 2 * state["dud"] != state["uud"] - 2 * state["udu"]:
            print(state)
            exit("Err")

        for l in labels:
            out += str(state[l]) + ","
        return out

    for config in list(itertools.product([-1, 1], repeat=L)):
        for i in range(L):
            grid.set(i, config[i])

        state = grid.count_states()
        state_key = get_state_key(state)
        if state_key not in state_counts:
            state_counts[state_key] = 0
        state_counts[state_key] += 1

    print(L, len(state_counts))
    counts.append(len(state_counts))
    print("a,b,c,d,e,f")
    for state in sorted(state_counts.keys(), reverse=True):
        s = state.split(",")
        # print(
        #     "{Out: " + str(state_counts[state]) + ", In: map[string]float64",
        #     '{"L": %s, "a": %s, "b": %s, "c": %s, "d": %s, "e": %s, "f": %s}' % (L, s[0], s[1], s[2], s[3], s[4], s[5]),
        #     "},",
        # )

        print(state, state_counts[state], energy(state), guess_multiplicity(L, state))
        assert state_counts[state] == guess_multiplicity(L, state)


def calculate_multiplicity(l):
    out = []
    current = [[l, 0, 0, 0, 0, 0]]
    rules = [
        [(3, 0, 0, 0, 0, 0), (0, 2, 0, 0, 0, 1)],
        [(2, 1, 0, 0, 0, 0), (0, 1, 1, 0, 0, 1)],
        [(1, 1, 0, 0, 0, 1), (0, 1, 0, 0, 2, 0)],
        [(1, 1, 0, 0, 1, 0), (0, 1, 0, 1, 1, 0)],
        [(0, 0, 1, 0, 0, 2), (0, 0, 0, 1, 2, 0)],
        [(0, 0, 1, 0, 1, 1), (0, 0, 0, 2, 1, 0)],
        [(0, 0, 1, 0, 2, 0), (0, 0, 0, 0, 0, 3)],
        [(1, 2, 0, 0, 0, 0), (0, 0, 2, 0, 0, 1)],
    ]

    # active = True
    while len(current) != 0:
        # active = False

        new_current = []

        for state in current:
            if state not in out:
                out.append(state)
            for rule in rules:

                is_valid = True
                for i in range(6):
                    if state[i] < rule[0][i]:
                        is_valid = False
                if is_valid:
                    # Apply rule
                    s = copy(state)

                    for j in range(6):
                        s[j] -= rule[0][j]
                        s[j] += rule[1][j]

                    if s == [1, 0, 2, 0, 2, 1]:
                        print(state)
                        print("HERE")
                        print(rule)

                    # if a not in new_current:
                    new_current.append(s)

        current = new_current
    return out


# print((calculate_multiplicity(6)))
