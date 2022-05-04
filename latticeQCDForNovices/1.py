import numpy as np
import math
from typing import List, Callable
import vegas
import matplotlib.pyplot as plot

a = 1.0 / 2
N = 8
E_0 = 1.0 / 2
m = 1
A = (m / 2 / math.pi / a) ** (N / 2)

x0 = xf = 0


def V(x):
    return x ** 2 / 2


def S_lat(x: List[float]):

    out = (m / 2 / a) * (x[1] - x0) ** 2 + a * V(x0)
    out += (m / 2 / a) * (xf - x[N - 2]) ** 2 + a * V(xf)
    for j in range(1, N - 2):
        out += (m / 2 / a) * (x[j + 1] - x[j]) ** 2 + a * V(x[j])
    return math.exp(-out)


integ = vegas.Integrator(
    [
        [-5, 5],
        [-5, 5],
        [-5, 5],
        [-5, 5],
        [-5, 5],
        [-5, 5],
        [-5, 5],
    ]
)
xs = []
ys = []
for x in np.linspace(0, 2, 10):
    xi = x
    xf = x
    result = integ(S_lat, nitn=100, neval=10000)

    xs.append(x)
    ys.append(A * result.mean)

    print(x, A * result.mean)

print(xs, ys)

plot.plot(xs, ys)
plot.show()
plot.pause(0)