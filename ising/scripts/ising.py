import math
import matplotlib.pyplot as plt
import random


class Ising:
    def __init__(self, gridSize: int, T: float):
        self.gridSize = gridSize
        self.T = T
        self.reset()

    def reset(self):
        self.i = 0
        self.grid = [[random.choice([-1, 1]) for i in range(self.gridSize)] for j in range(self.gridSize)]
        self.prevEnergy = self.calculateEnergy()

    def plot(self):
        plt.imshow(self.grid)
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

        if newEnergy < self.prevEnergy or random.random() < math.exp(-dE / self.T):
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
