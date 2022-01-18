from sympy import symbols
from sympy.plotting import plot, plot3d
import scipy.constants
import sympy

lambda_, T, pi, h, c, k = symbols('lambda T pi h c k')
constant_subs = [(pi, scipy.constants.pi), (h, scipy.constants.h), (c, scipy.constants.c), (k, scipy.constants.k)]

plank_distribution = 8 * sympy.pi * h * c / lambda_ ** 5 / (sympy.exp(h * c / (lambda_ * k * T)) - 1)
Ts = list(range(2000, 6000, 1000))

series = (plank_distribution.subs(constant_subs).subs(T, t) for t in Ts)
p1 = plot(
    *series,
    (lambda_, 0, 6 * 10 ** -6),
    show=False,
    legend=True,
    title="Plank Blackbody Radiation",
    xlabel="$ \lambda $                          ",
    ylabel="Intensity",
)

for i in range(len(Ts)):
    p1[i].label = f'$T={Ts[i]}$'

p1.show()
