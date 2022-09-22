import math
from re import A
import sympy


# a.) find equation for altitude h of a satellite
h, G, M, T, R, m, v, pi = sympy.symbols("h G M T R m v pi", real=True, positive=True)

constants = {G: 6.67e-11, M: 5.97e24, R: 6371000, pi: math.pi}  # m^3 kg^-1 s^-2  # kg  # meters

f = (-1) * G * M * m / (h) ** 2 + m * (v) ** 2 / (h)
vEq = 2 * pi * (h) / T
f = f.subs(v, vEq)
solution = (
    sympy.solve(f, h)[0] - R
)  # Frustratingly sympy can't handle if we use R+h, so just put that back in later. Strangely mathematica didn't like it either...?
sympy.pretty_print(solution)

# b.) Ask user for T

# T_input = input("What is your T(s): ")
# print(solution.subs(constants).subs(T, T_input).evalf())


def calculate_altitude(period):
    return solution.subs(constants).subs(T, period).evalf()


# c.) Calculate some orbits

print(f"T=1d h={calculate_altitude(24 * 60 * 60)}")
print(f"T=90min h={calculate_altitude(90 * 60)}")
print(f"T=45min h={calculate_altitude(45 * 60)}")

# It is not possible to have a stable 45min orbit

# d.) Why sidereal day?

# We define a day as how long it takes for the sun to be in the same spot
# We spin once every 24 hours, but we're also moving around the sun at the same time.

# A fun simple check, if the earth wasn't internally rotating, our 'day' would take one year as we rotate around the sun.
# sidereal day is 4 minutes shorter per day, so over 365 days, it should account for 24 hours
# 4 (mins/day) * 365 (days) / 60 (mins/hour) / (24 hours/day) = 1 day

normal_period = calculate_altitude(24 * 60 * 60)
sidereal_period = calculate_altitude(23.93 * 60 * 60)

print(
    f"Difference due to sidereal day: {normal_period-sidereal_period:.02f}m. Which is a difference of {100*(normal_period-sidereal_period)/normal_period}%"
)
