import math
import matplotlib.pyplot as plt
import random
import numpy as np
from numba import int64, float64
from numba.experimental import jitclass


spec = [
    ("i", int64),
    ("T", float64),
    ("gridSize", int64),
    ("prevEnergy", float64),
    ("grid", int64[:, :]),
]


def plot(grid):
    plt.imshow(grid)
    plt.show()


@jitclass(spec=spec)
class Ising:
    def __init__(self, gridSize: int, T: float):
        self.gridSize = int(gridSize)
        self.T = T
        self.reset()

    def reset(self):
        self.i = 0
        self.grid = np.random.choice(np.asarray([-1, 1]), size=(self.gridSize, self.gridSize))
        self.prevEnergy = self.calculateEnergy()

    def plot(self):
        plt.imshow(self.grid)
        plt.show()

    def plot_interations(self):
        interation_grid = [[0 for i in range(self.gridSize * 2)] for j in range(self.gridSize * 2)]

        for x_i in range(0, 2 * self.gridSize):
            for y_i in range(0, 2 * self.gridSize):
                if x_i % 2 == y_i % 2:
                    continue

                x = int(x_i / 2)
                y = int(y_i / 2)

                if y_i % 2 == 1:
                    interation_grid[x_i][y_i] = 1 if self.at(x - 1, y) == self.at(x, y) else -1
                if x_i % 2 == 1:
                    interation_grid[x_i][y_i] = 1 if self.at(x, y - 1) == self.at(x, y) else -1

                #  = 0 if self.at(x + 1, y) == self.at(x, y) else 1
        plt.imshow(interation_grid, cmap='coolwarm')
        plt.show()

    def at(self, x: int, y: int) -> int:
        return self.grid[x % self.gridSize][y % self.gridSize]

    def calculateEnergy(self) -> float:
        out = 0
        for i in range(self.gridSize):
            for sweep in range(self.gridSize):
                out += -self.at(i, sweep) * self.at(i + 1, sweep)
                out += -self.at(sweep, i) * self.at(sweep, i + 1)
        return out

    def calculateMagnatism(self) -> float:
        out = 0
        for x in range(self.gridSize):
            for y in range(self.gridSize):
                out += self.at(x, y)

        return out / (self.gridSize * self.gridSize)

    def step(self):
        x = int(self.gridSize * random.random())
        y = int(self.gridSize * random.random())

        self.grid[x][y] *= -1

        spot = self.at(x, y)

        dE = 0
        dE -= self.at(x - 1, y) + self.at(x + 1, y) + self.at(x, y + 1) + self.at(x, y - 1)
        dE *= spot * 2

        newEnergy = self.prevEnergy + dE

        if newEnergy <= self.prevEnergy or random.random() < math.exp(-dE / self.T):
            self.prevEnergy = newEnergy
        else:
            self.grid[x][y] *= -1

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
                if self.at(x, y) == self.at(x, y + 1):
                    out += 1
                if self.at(x, y) == self.at(x, y - 1):
                    out += 1
                total += out / 4
        return total / self.gridSize ** 2

    def calculateDisorder(self):
        clumpy = 0
        halfGrid = int(self.gridSize / 2)
        for x in range(0, self.gridSize):
            for y in range(0, self.gridSize):
                for dx in range(-halfGrid, halfGrid):
                    for dy in range(-halfGrid, halfGrid):
                        if dx == 0 and dy == 0:
                            continue
                        distance = math.sqrt(dx * dx + dy * dy)

                        if self.at(x, y) != self.at((x + dx) % self.gridSize, (y + dy) % self.gridSize):
                            clumpy += math.exp(-distance)

                        # else:
                        # clumpy -= distance
        return clumpy

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


if __name__ == "__main__":

    import time

    gridS = 128
    m = Ising(gridS, 2)

    Ts = [x / 10.0 for x in range(1, 50, 1)]
    print(Ts)
    # Ts = np.arange(0.1, 4, 0.2)
    Cs = []
    Ms = []

    fig = plt.figure(constrained_layout=True, figsize=(10, 10))

    i = 1

    steps = 1000000000

    for t in Ts:
        print(t)
        m.reset()
        m.T = t

        m.loop(steps)

        Cs.append(abs(m.calculateCorrelation()))
        Ms.append(abs(m.calculateMagnatism()))

        ax = fig.add_subplot(math.ceil(len(Ts) / 7), 7, i)
        ax.imshow(m.grid)
        ax.axis('off')
        ax.set_title(f'T={t}')
        i += 1

        # m.plot()

        # time.sleep(1)

    fig.suptitle(f'2D Ising: Steps={steps}, Grid={gridS}')
    plt.show()
    plt.close()

    # plt.figure()
    plt.plot(Ts, Cs, label="Correlation")
    plt.plot(Ts, Ms, label="Magnetism")
    plt.title(f'2D Ising: Steps={steps}, Grid={gridS}')
    plt.legend()
    plt.show()