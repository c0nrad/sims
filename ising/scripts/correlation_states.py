import math
import matplotlib.pyplot as plt
import random

from ising import Ising
import time

gridSize = 512 * 4
m = Ising(gridSize, 2.269185)

m.loop(1000000000)

# m.plot()

states = {}
for x in range(gridSize):
    for y in range(gridSize):
        state = [m.at(x, y), m.at(x + 1, y), m.at(x - 1, y), m.at(x, y + 1), m.at(x, y - 1)]

        state = ["0" if item == -1 else str(item) for item in state]

        if "".join(state) in states:
            states["".join(state)] += 1
        else:
            states["".join(state)] = 1


nearestCorrelation = m.calculateCorrelation()
print("nearestCorrelation", nearestCorrelation)

zero_opposed = ["00000"]
one_opposed = ["00001", "00010", "00100", "01000"]
two_opposed_adjecent = ["00011", "01100", "00110", "01001"]
two_opposed_opposite = ["00101", "01010"]
three_opposed = ["00111", "01110", "01011", "01101"]
four_opposed = ["01111"]

all_states = set(
    zero_opposed + one_opposed + two_opposed_adjecent + two_opposed_opposite + three_opposed + four_opposed
)
assert len(all_states) == 16
for a in all_states:
    assert len(a) == 5, a


def invert_state(state):
    return "".join(["0" if s == "1" else "1" for s in state])


state_groups = [zero_opposed, one_opposed, two_opposed_adjecent, two_opposed_opposite, three_opposed, four_opposed]
merged_states = {"00000": 0, "00001": 0, "00011": 0, "00101": 0, "00111": 0, "01111": 0}
for state in states:
    for group in state_groups:
        if state in group or invert_state(state) in group:
            merged_states[group[0]] += states[state]

print(merged_states)
totalSpots = sum([merged_states[group[0]] for group in state_groups])
assert totalSpots == gridSize ** 2
print("totalSpots", totalSpots)
for state in merged_states:
    print(state, merged_states[state] / totalSpots)

totalP = 0
totalStates = 0
for state in states:
    if state[0] != "0":
        continue
    color = state[0]
    p = 1
    for c in state[1:]:
        if c == color:
            p *= nearestCorrelation
        if c != color:
            p *= 1 - nearestCorrelation

    invertedState = "".join(["0" if item == "1" else "1" for item in state])

    if invertedState not in states:
        states[invertedState] = 0

    totalP += p
    totalStates += (states[state] + states[invertedState]) / (gridSize * gridSize)
    print(state, (states[state] + states[invertedState]) / (gridSize * gridSize), p)

print("totalP", totalP)
print("totalStates", totalStates)
