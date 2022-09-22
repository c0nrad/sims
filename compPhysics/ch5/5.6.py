import numpy as np
import matplotlib.pyplot as plot


def integrate_trapezoidal(f, a, b, N):
    h = (b - a) / N

    out = 0.5 * (f(a) + f(b))
    for k in range(1, N):
        out += f(a + k * h)

    return h * out


def f(x):
    return x ** 4 - 2 * x + 1


def error_trapezoidal(i1, i2):
    return (i2 - i1) / 3


a = 0
b = 2

x = []
y = []
err = []

for i in range(1, 5):
    N_small = 10 ** i
    N_big = 10 ** (i + 1)
    x.append(N_big)

    I_small = integrate_trapezoidal(f, a, b, N_small)
    I_big = integrate_trapezoidal(f, a, b, N_big)
    y.append(I_big)

    e2 = error_trapezoidal(I_small, I_big)
    err.append(e2)

    print(f"N_small={N_small}, N_big={N_big}, I_small={I_small}, I_big={I_big}, e2={e2}")


plot.errorbar(x, y, err)
plot.xscale('log', base=10)

plot.show()
plot.pause(0)

# The correct value is within error. The error is scaled by a constant c, so it's not going to be exact, just within the bounds.
