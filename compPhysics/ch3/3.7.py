import cmath
import math
import numpy as np
import matplotlib.pyplot as plot

ITERATIONS = 100
Z = 0
N = 1000
L = 4


def magnitude(x, y):
    z = complex(0, 0)
    for i in range(ITERATIONS):
        z = z ** 2 + complex(x, y)
        mag = math.sqrt(z.real ** 2 + z.imag ** 2)

        if mag > 2:
            return i
    return i


out = np.full((N, N), 0)
for x_i in range(N):
    for y_i in range(N):
        x = (-L / 2) + (L * x_i / N)
        y = (-L / 2) + (L * y_i / N)

        out[y_i][x_i] = magnitude(x, y)

plot.matshow(out)
plot.show()
plot.pause(0)
