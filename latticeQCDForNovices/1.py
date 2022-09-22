import numpy as np
import math
from typing import List, Callable
import vegas
import matplotlib.pyplot as plot

a = 1.0 / 2  # Grid Spacing
N = 8  # Number of Time Slices
m = 1  # Mass
A = (m / 2.0 / math.pi / a) ** (N / 2)  # Normalization Constant for Integration
T = a * N  # Total time
span = 5  # integration range


def calculate_exact_qho_groundstate(x):
    T = a * N
    E_0 = 1.0 / 2
    wave_function = math.exp(-(x * x) / 2.0) / math.pi ** (1 / 4.0)
    return wave_function ** 2 * np.exp(-E_0 * T)


def V_ho(x):
    return x ** 2 / 2.0


def V_aho(x):
    return x ** 4 / 2.0


def integrand(xi, xf, V) -> Callable:
    def S_lat(x: List[float]):
        kinetic = sum((x[1:] - x[:-1]) ** 2) + (x[0] - xi) ** 2 + (xf - x[-1]) ** 2
        kinetic *= m / 2.0 / a
        potential = a * (sum(V(x)) + V(xi))  # No V(xf)

        return kinetic + potential

    return lambda x: np.exp(-S_lat(x))


integ = vegas.Integrator([[-span, span]] * (N - 1))
xs = []
ys = []
solns = []
for x in np.linspace(0, 2, 10):
    xi = x
    xf = x

    integ(integrand(x, x, V_ho), nitn=5, neval=10000)
    result = integ(integrand(x, x, V_ho), nitn=100, neval=10000)

    xs.append(x)
    ys.append(A * result.mean)
    solns.append(calculate_exact_qho_groundstate(x))
    print(xs[-1], ys[-1], solns[-1])

plot.plot(xs, ys, "o", label="path integral")
plot.plot(xs, solns, label="analytics (solution)")
plot.xlabel("x")
plot.ylabel(r"$\langle x | e^{-HT} | x \rangle $")
plot.legend()
plot.show()
plot.pause(0)