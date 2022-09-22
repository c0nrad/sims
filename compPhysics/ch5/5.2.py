import math


def f(x):
    return x ** 4 - 2 * x + 1


def integrate_simpson(f, N, a, b):
    h = (b - a) / N

    out = f(a) + f(b)
    for k in range(1, N):
        if k % 2 == 0:
            out += 2 * f(a + k * h)
        else:
            out += 4 * f(a + k * h)

    return out * h / 3.0


for N in [10, 100, 1000, 10000, 100000]:
    print(f"integrate_simpson(f, {N}, 0.0, 2.0): {integrate_simpson(f, N, 0.0, 2.0)}")

    guess = integrate_simpson(f, N, 0.0, 2.0)

    print(f"error: {abs(4.4 - guess) * 100 / 4.4}")

# significantly better than trap methods
