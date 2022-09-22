import math
import random
import numpy as np
from numba import int64, float64, int8
from numba.experimental import jitclass
import colorama
from scipy.optimize import curve_fit
from copy import copy, deepcopy
import matplotlib.pyplot as plot

from utils import normalize_states, value_to_ud


spec = [
    ("i", int64),
    ("T", float64),
    ("gridSize", int64),
    ("prevEnergy", float64),
    ("grid", int64[:]),
]


# @jitclass(spec=spec)
class Ising1D:
    def __init__(self, gridSize: int, T: float):
        self.gridSize = int(gridSize)
        self.T = T
        self.reset()

    def reset(self):
        self.i = 0
        self.grid = np.random.choice(np.asarray([-1, 1]), size=(self.gridSize))
        self.prevEnergy = self.calculateEnergy()

    def at(self, x: int) -> int:
        return self.grid[x % self.gridSize]

    def state_at(self, x: int) -> str:
        state = (
            self.at(x - 1),
            self.at(x),
            self.at(x + 1),
        )

        return "".join([value_to_ud(a) for a in state])

    def set(self, x: int, v: int) -> int:
        self.grid[x % self.gridSize] = v

    def equals(self, other) -> bool:
        # return np.array_equal(self.grid, other.grid)
        if self.gridSize != other.gridSize:
            return False
        for x in range(self.gridSize):
            if self.at(x) != other.at(x):
                # print(self.at(x, y), other.at(x, y))
                return False

        return True

    def to_line(self) -> str:
        out = ""
        for x in range(self.gridSize):
            out += value_to_ud(self.at(x))
        return out

    def clone(self):
        out = Ising(self.gridSize, self.T)
        # out.grid = [row[:] for row in self.grid]
        # out.grid = deepcopy(self.grid)
        out.grid = np.array(self.grid, copy=True)
        return out

    def calculateEnergy(self) -> float:
        out = 0
        for i in range(self.gridSize):
            out += -self.at(i) * self.at(i + 1)
        return out

    def calculateMagnatism(self) -> float:
        return sum(self.grid) / (self.gridSize)

    def calculateEntropy(self) -> float:
        out = 0
        states = self.count_normalized_states()
        # states = {k: v / self.gridSize for (k, v) in states.items() if v != 0}

        # if "duu" in states and "uud" in states:
        # states["uud"] = states["duu"] + states["uud"]
        # states["udu"] = [sum(value) for value in zip(results["ddu"], results["udd"])]

        # print(states)
        for state in ["duu", "dud"]:
            if state not in states:
                continue
            out -= states[state] * np.log(states[state])
            # print(states[states], np.log(states[states]))
        return out

    def step(self):
        x = int(self.gridSize * random.random())

        self.grid[x] *= -1

        spot = self.at(x)

        dE = 0
        dE -= self.at(x - 1) + self.at(x + 1)
        dE *= spot * 2

        newEnergy = self.prevEnergy + dE

        if newEnergy < self.prevEnergy or random.random() < math.exp(-dE / self.T):
            self.prevEnergy = newEnergy
        else:
            self.grid[x] *= -1

        # self.i += 1

    def loop(self, steps):
        for i in range(steps):
            self.step()
        self.i += steps

        assert self.calculateEnergy() == self.prevEnergy

    def calculateCorrelation(self):
        total = 0
        for x in range(self.gridSize):
            for y in range(self.gridSize):
                out = 0
                if self.at(x, y) == self.at(x + 1, y):
                    out += 1
                if self.at(x, y) == self.at(x - 1, y):
                    out += 1
                total += out / 4
        return total / self.gridSize

    def calculateCorrelationFunction(self):
        out = np.zeros(self.gridSize // 2 - 1)
        for x in range(0, self.gridSize):
            for y in range(0, self.gridSize):
                for r in range(0, int(self.gridSize // 2 - 1)):
                    out[r] += (
                        self.at(x, y)
                        * (self.at(x + r, y) + self.at(x, y + r) + self.at(x - r, y) + self.at(x, y - r))
                        / 4
                    )
        out /= self.gridSize * self.gridSize
        # print("Before subtracting magnatism", out[0:10], self.calculateMagnatism())
        out -= self.calculateMagnatism() ** 2
        # print("After/ subtracintg magnatism", out[0:10])
        return np.abs(out)

    def dump(self):
        out = ""

        for x in range(self.gridSize):
            if self.at(x) == 1:
                out += "u"
            elif self.at(x) == -1:
                out += "d"
            else:
                out += "0"
        print(out)

    def calculateCorrelationDistance(self):
        def exponential_fit(x, g, a):
            return a * np.exp(-((x) / g))

        # print(exponential_fit, list(range(self.gridSize // 2 - 1)), self.calculateCorrelationFunction())
        return curve_fit(exponential_fit, range(self.gridSize // 2 - 1), self.calculateCorrelationFunction())[0][0]

    def count_states(self):
        out = {"uuu": 0, "uud": 0, "udu": 0, "udd": 0, "duu": 0, "dud": 0, "ddu": 0, "ddd": 0}
        for i in range(self.gridSize):
            state = self.value_to_ud(self.at(i)) + self.value_to_ud(self.at(i + 1)) + self.value_to_ud(self.at(i + 2))
            if state not in out:
                out[state] = 0
            out[state] += 1

        out["uud"] = out["uud"] + out["duu"]
        del out["duu"]
        out["ddu"] = out["ddu"] + out["udd"]
        del out["udd"]
        return out

    def count_normalized_states(self):
        states = self.count_states()

        # states["duu"] += states["uud"]
        # states["ddu"] += states["udd"]
        # del states["uud"]
        # del states["udd"]

        return {k: v / self.gridSize for (k, v) in states.items()}

    def value_to_ud(self, v: int) -> str:
        if v == -1:
            return "d"
        if v == 1:
            return "u"
        if v == 0:
            return "0"
        print(v)
        raise Exception("invaluid ud")


def is_rotate_equal(a, b):
    l = len(a)
    for offset in range(len(a)):
        equal = True
        for j in range(len(a)):
            if a[(offset + j) % l] != b[j]:
                equal = False
                break

        if equal:
            return True
    return False


assert is_rotate_equal([1, 1, 1, 1], [1, 1, 1, 1])
assert is_rotate_equal([0, 1, 1, 1], [1, 0, 1, 1])
assert not is_rotate_equal([1, 0, 1, 0], [1, 1, 1, 0])


if __name__ == "__main__":

    import time

    gridS = 500
    model = Ising(gridS, 2)

    Ts = np.linspace(2, 0.1, 20)

    steps = 1000000

    results = {}

    for t in Ts:
        print(t)
        model.T = t

        iterations = 200

        avg_states = {}
        for _ in range(iterations):
            model.loop(steps)

            states = model.count_states()

            # Break symmetry
            if states["uuu"] < states["ddd"]:
                states["uuu"], states["ddd"] = states["ddd"], states["uuu"]
                states["uud"], states["ddu"] = states["ddu"], states["uud"]
                states["udd"], states["duu"] = states["duu"], states["udd"]
                states["udu"], states["dud"] = states["dud"], states["udu"]

            for state in states:
                if state not in avg_states:
                    avg_states[state] = []
                avg_states[state].append(states[state] / gridS)

        for state in avg_states:
            if state not in results and "_err" not in state:
                results[state] = []
                results[state + "_err"] = []
            results[state].append(sum(avg_states[state]) / iterations)
            results[state + "_err"].append(np.std(avg_states[state]))

    print(results)
    for state in results:
        if "_err" not in state:
            # if state[0] == "u":
            plot.errorbar(Ts, results[state], yerr=results[state + "_err"], label=state)
    plot.legend(loc="upper right")

    plot.show()
