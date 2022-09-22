from cmath import inf
import numpy as np

from timeit import default_timer as timer


def integrate_trapezoidal(f, a, b, N):
    h = (b - a) / N

    out = 0.5 * (f(a) + f(b))
    for k in range(1, N):
        out += f(a + k * h)

    return h * out


# def integrate_adaptive_trapezoidal_step(f, a, b, N, i_prev):


def error_trapezoidal(i1, i2):
    return (i2 - i1) / 3


def f(x):
    return np.sin(np.sqrt(100 * x)) ** 2


def integrate_adaptive_trapezoidal(f, a, b, epsilon):
    N_small = 0
    N_big = 1

    i_small = 0
    i_big = epsilon * 10

    error = epsilon * 2

    while abs(error) > epsilon:
        # print(f"N_small={N_small}, N_big={N_big}, i_small={i_small}, i_big={i_big}, error={error}")
        N_small = N_big
        i_small = i_big
        N_big = 2 * N_big

        i_big = integrate_trapezoidal(f, a, b, N_big)
        error = error_trapezoidal(i_small, i_big)
        print(f"N_small={N_small}, N_big={N_big}, i_small={i_small}, i_big={i_big}, error={error}")

    return i_big


def integrate_adaptive_trapezoidal2(f, a, b, epsilon):
    N_prev = 0
    N_curr = 1

    i_prev = 0
    i_curr = (f(a) + f(b)) / 2.0

    error = error_trapezoidal(i_prev, i_curr)
    # error = epsilon * 2

    while abs(error) > epsilon:
        N_prev = N_curr
        N_curr = 2 * N_curr
        i_prev = i_curr
        h = (b - a) / N_curr

        i_curr = 0
        for k in range(1, N_curr, 2):
            i_curr += f(a + k * h)
        i_curr = h * i_curr + i_prev / 2.0

        error = error_trapezoidal(i_prev, i_curr)
        print(f"N_small={N_prev}, N_big={N_curr}, i_small={i_prev}, i_big={i_curr}, error={error}")

    return i_curr


start = timer()
print(integrate_adaptive_trapezoidal(f, 0, 1, 1e-6))
end = timer()
print(end - start)

start = timer()
print(integrate_adaptive_trapezoidal2(f, 0, 1, 1e-6))
end = timer()
print(end - start)

# The second one is twice as fast, which makes sense


# b.)
