import math
import numpy as np
import matplotlib.pyplot as plot


def f(t):
    return np.exp(-(t ** 2))


def integrate_simpson(f, N, a, b):
    h = (b - a) / N

    out = f(a) + f(b)
    for k in range(1, N):
        if k % 2 == 0:
            out += 2 * f(a + k * h)
        else:
            out += 4 * f(a + k * h)

    return out * h / 3.0


# a/b

xs = np.linspace(0.1, 3, 30)
ys = np.zeros(30)
i = 0
for x in xs:
    ys[i] = integrate_simpson(f, 100, 0, x)
    print(f"E({x:.01f})={ys[i]:.04f}")
    i += 1

print(ys)
plot.plot(xs, ys, label="E(x)")
plot.plot(xs, f(xs), label="f(x)")
plot.legend()
plot.show()
plot.pause(0)
