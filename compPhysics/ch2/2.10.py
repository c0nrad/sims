# Semi-Empircal Mass Formula


def calc_nuclear_binding_energy(Z, A):
    a1 = 15.8
    a2 = 18.3
    a3 = 0.714
    a4 = 23.2
    a5 = 0

    if A % 2 == 0 and Z % 2 == 0:
        a5 = 12
    if A % 2 == 0 and Z % 2 == 1:
        a5 = -12

    return a1 * A - a2 * A ** (2 / 3) - a3 * Z * Z / A ** (1 / 3) - a4 * (A - 2 * Z) ** 2 / A + a5 / A ** (1 / 2)


def calc_nuclear_binding_energy_per_nucleon(Z, A):
    return calc_nuclear_binding_energy(Z, A) / A


print(f'Binding Energy of A=58 and Z=28, B={calc_nuclear_binding_energy(28, 58)}')
print(f'Binding Energy per nucleon of A=58 and Z=28, B={calc_nuclear_binding_energy_per_nucleon(28, 58)}')

# (c)
# Z = 28
# for A in range(Z, 3 * Z):
#     print(Z, A, calc_nuclear_binding_energy_per_nucleon(Z, A))

# (d) find most stable binding energy per atom


def calc_stable_mass(Z):
    max_b = 0
    max_a = 0
    for A in range(Z, 3 * Z):
        new_b = calc_nuclear_binding_energy_per_nucleon(Z, A)
        if new_b > max_b:
            max_b = new_b
            max_a = A

    return max_a, max_b


for A in range(1, 100):
    print(A, calc_stable_mass(A))

# Max is 28, nickel
