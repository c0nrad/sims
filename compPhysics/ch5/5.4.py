import numpy as np
import matplotlib.pyplot as plot


def Jm_function(m, x):
    return lambda theta: np.cos(m * theta - x * np.sin(theta)) / np.pi


def integrate_simpson(f, N, a, b):
    h = (b - a) / N

    out = f(a) + f(b)
    for k in range(1, N):
        if k % 2 == 0:
            out += 2 * f(a + k * h)
        else:
            out += 4 * f(a + k * h)

    return out * h / 3.0


# a
# N = 1000
# xs = np.linspace(0, 20, N)

# J0 = np.zeros(N)
# J1 = np.zeros(N)
# J2 = np.zeros(N)

# i = 0
# for x in xs:
#     J0[i] = integrate_simpson(Jm_function(0, x), 1000, 0, np.pi)
#     J1[i] = integrate_simpson(Jm_function(1, x), 1000, 0, np.pi)
#     J2[i] = integrate_simpson(Jm_function(2, x), 1000, 0, np.pi)

#     i += 1

# plot.plot(xs, J0)
# plot.plot(xs, J1)
# plot.plot(xs, J2)
# plot.show()
# plot.pause(0)

# # b
wavelength = 500e-9
k = 2 * np.pi / wavelength

a = -1e-6
b = 1e-6
N = 100


def I(r):
    if r == 0:
        return 1.0 / 4.0
    return (integrate_simpson(Jm_function(0, k * r), 100, 0, np.pi) / k / r) ** 2


data = np.zeros((N, N))

for xi in range(N):
    print(xi)
    for yi in range(N):
        x = a + xi * (b - a) / N
        y = a + yi * (b - a) / N

        r = np.sqrt(x * x + y * y)
        data[xi][yi] = I(r)

plot.matshow(data, vmax=0.01)
# plot.show()
plot.pause(0)
