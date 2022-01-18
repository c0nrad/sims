from sympy import symbols, diff, simplify, solve, nsolve, lambdify, init_printing, pprint, latex
from sympy.plotting import plot, plot3d
import scipy.constants
import sympy

init_printing()

lambda_, T, pi, h, c, k = symbols('lambda T pi h c k')
constant_subs = [(pi, scipy.constants.pi), (h, scipy.constants.h), (c, scipy.constants.c), (k, scipy.constants.k)]

plank_distribution = 8 * pi * h * c ** 2 / lambda_ ** 5 / (-1 + sympy.exp(h * c / (lambda_ * k * T)))

print(latex(plank_distribution))

print("Plank Distribution")
pprint(plank_distribution)


print("After diff")
eq1 = diff(plank_distribution, lambda_)
pprint(eq1)
print(latex(eq1))

u = symbols('u')
eq2 = eq1.subs(c * h / (T * k * lambda_), u)
print("Eq2=")
pprint(eq2)

eq3 = solve(eq2, u)[0]
print("u=")
pprint(eq3)
print(latex(eq3))
print(eq3.n())

print("wien's law, lambda=")
pprint(solve(c * h / (T * k * lambda_) - eq3.n(), lambda_)[0].subs(constant_subs))
