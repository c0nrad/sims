import math
import decimal


def quadratic_formula(a, b, c):
    discriminate = b * b - 4 * a * c

    return ((-b + math.sqrt(discriminate) / (2 * a)), (-b - math.sqrt(discriminate) / 2))


print("Solution for .001x^2 + 1000x + .001 = 0")
print(quadratic_formula(0.001, 1000, 0.001))


def quadratic_formula_v2(a, b, c):
    discriminate = b * b - 4 * a * c

    soln1 = (2 * c) / (-b - math.sqrt(discriminate))
    soln2 = (2 * c) / (-b + math.sqrt(discriminate))
    return (soln1, soln2)


def quadratic_formula_v3(a: decimal.Decimal, b: decimal.Decimal, c: decimal.Decimal):
    discriminate = b * b - 4 * a * c

    soln1 = (-b + decimal.Decimal.sqrt(discriminate)) / (2 * a)
    soln2 = (-b - decimal.Decimal.sqrt(discriminate)) / (2 * a)
    return (soln1, soln2)


print("Solution 2 for .001x^2 + 1000x + .001 = 0")
print(quadratic_formula_v2(0.001, 1000, 0.001))


print("Solution 3 for .001x^2 + 1000x + .001 = 0")
print(quadratic_formula_v3(decimal.Decimal(0.001), decimal.Decimal(1000), decimal.Decimal(0.001)))