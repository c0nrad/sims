import sympy
import itertools

pb, T = sympy.symbols("pb T", real=True, positive=True)

print(id(pb), id(T))
total = 0.0

towards_black = 0
towards_white = 0
do_nothing = 0

for state in itertools.product([0, 1], repeat=5):
    p = 1
    for c in state:
        if c == 1:
            p *= pb
        if c == 0:
            p *= 1 - pb

    dE = 0
    if state[0] == 0:
        dE = 2 * state[1:].count(0) + -2 * state[1:].count(1)
    if state[0] == 1:
        dE = -2 * state[1:].count(0) + 2 * state[1:].count(1)

    # print(str(state[0]), "".join([str(i) for i in state[1:]]), p, dE)
    total += p

    # Towards Black
    if state[0] == 0:
        if dE < 0:
            towards_black += p
        else:
            towards_black += p * (sympy.exp(-dE / T))

    # Do nothing
    if dE >= 0:
        do_nothing += p * (1 - sympy.exp(-dE / T))
        # towards_black += p * (1 - math.exp(-dE / T))

    # Towards White
    if state[0] == 1:
        if dE < 0:
            towards_white += p
        else:
            towards_white += p * (sympy.exp(-dE / T))

expr = towards_black / (1 - do_nothing)

# print("C Solution?")
# tc = sympy.simplify(expr.subs([(T, 2 / sympy.ln(1 + sympy.sqrt(2)))]))

# # sympy.plot(tc, (pb, 0.01, 0.99))
# dtc = sympy.diff(tc, pb)

# # sympy.plot(dtc, (pb, 0.01, 0.99))

# print(sympy.nsolve(sympy.diff(dtc, pb), pb, 0.2))

# exit(0)
from sympy.plotting import plot3d

# plot3d(expr, (pb, 0.01, 0.99), (T, 2, 2.5))

sympy.pprint(expr)
print(expr)
d1 = sympy.diff(expr, pb)
print("d1=")
sympy.pprint(d1)

d2 = sympy.diff(d1, pb)
print("d2=")
sympy.pprint(d2)

# for t in [2.1, 2.2, 2.3, 2.4, 2.5, 2.6]:
# print(sympy.nsolve(d1.subs(T, 1), pb, 0.1, verify=False))
# sympy.plot(d1.subs(T, t), (pb, 0, 1))


# solve([x >= 0.5, x <= 3, x ** 2 - 1], x)

pb, T = sympy.symbols("pb T", real=True, positive=True)

print(id(T), id(pb))

print(sympy.nonlinsolve([d1, d2, pb > 0, pb < 100, T > 0, T < 5], (pb, T), (20, 2.5)))

# sympy.pprint(sympy.simplify(d1.subs(T, 2.00 / sympy.ln(1 + sympy.sqrt(2)))))
# print(sympy.solveset(d1, pb))
# print(sympy.nsolve(d2.subs(T, 1.7 / sympy.ln(1 + sympy.sqrt(2))), pb, 0.01, check=False))

# sympy.plot(expr.subs(T, 2.001 / sympy.ln(1 + sympy.sqrt(2))), (pb, 0, 1))

# sympy.plot(d1.subs(T, 2), (pb, 0, 1))


# plot3d(d1, (pb, 0.05, 0.3), (T, 2, 2.5))

# print("\n".join([str(a) for a in sympy.solve(d2, T, check=False)]))

exit(1)


print(d2)
sympy.pprint(sympy.solve(d2, T))


exit(1)
