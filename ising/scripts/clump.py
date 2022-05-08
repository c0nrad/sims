from ising import Ising
import numpy as np

# for t in np.linspace(0.1, 5, 20):
# t = 3
# model = Ising(4, t)

# model.loop(100)

# print("Clump time")
# print(f'T={t}, clump={model.calculateDisorder()}')
# model.plot()
# model.plot_interations()


gridSize = 5
model = Ising(gridSize, 0)

model.grid = [[0 for i in range(gridSize)] for j in range(gridSize)]
model.grid[2][2] = 1

print("Clump 1")
print(f'clump={model.calculateDisorder()}')
model.plot()

model.grid[2][3] = 1

print("Clump 2")
print(f'clump={model.calculateDisorder()}')
model.plot()

model.grid[2][3] = 0
model.grid[2][4] = 1

print("Clump gap")
print(f'clump={model.calculateDisorder()}')
model.plot()

model.grid[2][4] = 0
model.grid[3][3] = 1

print("Clump tri")
print(f'clump={model.calculateDisorder()}')
model.plot()


for x in range(gridSize // 2, gridSize):
    for y in range(0, gridSize):
        model.grid[x][y] = 1


print("Clump tri")
print(f'clump={model.calculateDisorder()}')
model.plot()
