import matplotlib.pyplot as plt
import numpy as np
import random

probabilityBlack = 0.8
probabilitySameColor = 0.8
gridSize = 100


probabilityBlack = 0.5
probabilitySameColor = 0.98


def generateGrid():
    grid = np.zeros((gridSize, gridSize))
    previous = 1

    for x in range(gridSize):
        for y in range(gridSize):

            if random.random() < probabilitySameColor:
                grid[x][y] = previous
            else:
                previous *= -1
                grid[x][y] = previous

    return grid


grid = generateGrid()

plt.imshow(grid)
plt.show()
