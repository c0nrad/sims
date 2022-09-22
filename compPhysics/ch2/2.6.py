import math

M = 1.981e30  # kg
G = 6.6738e-11  # m^3 kg^-1 s^-2

earth_l1 = 1.47e11  # m
earth_v1 = 3.0287e4  # m/s
earth_m = 5.972e24  # kg


halley_l1 = 8.7830e10  # m
halley_v1 = 5.4529e4  # m/s
halley_m = 2.2e14

# (a), why is it the smaller root of quadratic?

# The quadratic solution for v2 returns (-v1, -v2). You can show that the positive discriminant returns v1. Leaving the smaller solution to be v2.

# (b)(c) calculate a bunch of values for earth/halleys orbit


def calculate_v2(l1, v1):
    discriminant = (G * G * M * M / (v1 * l1) ** 2) + (v1 * v1) - (2 * G * M / l1)

    return (G * M / (v1 * l1)) - math.sqrt(discriminant)


def calculate_l2(l1, v1, v2):
    return l1 * v1 / v2


def calculate_energy(l, v, m):
    return 1 / 2 * m * v * v - G * m * M / l


def calculate_stats(l1, v1, m):

    print(f'v1={v1:.02f}, l1={l1:.02f}')
    print(f'E={calculate_energy(l1, v1, m)}')

    v2 = calculate_v2(l1, v1)
    l2 = calculate_l2(l1, v1, v2)

    print(f"v2={v2:.02f}, l2={l2:.02f}")
    print(f'E_sanity={calculate_energy(l2, v2, m)}')

    a = 0.5 * (l1 + l2)
    b = math.sqrt(l1 * l2)
    T = 2 * math.pi * a * b / (l1 * v1)
    e = (l2 - l1) / (l2 + l1)

    print(f"a={a:.01f}, b={b:.01f}, T={T:.01f}, e={e:.01f}")
    print(f"T_year={T/60/60/24/365}")


print("---Earth---")
calculate_stats(earth_l1, earth_v1, earth_m)

print("\n---Halley---")
calculate_stats(halley_l1, halley_v1, halley_m)

# hmmm, halley's orbit seems a little big
