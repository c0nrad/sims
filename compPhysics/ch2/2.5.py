import math

m = 9.1e-31  # kg
ev_to_j = 1.602e-19
E = 10 * ev_to_j  # j
V = 9 * ev_to_j  # j
hbar = 1.0545e-34  # m^2 kg/s

k1 = math.sqrt(2 * m * E) / hbar
k2 = math.sqrt(2 * m * (E - V)) / hbar

T = 4 * k1 * k2 / (k1 + k2) ** 2
R = ((k1 - k2) / (k1 + k2)) ** 2

print(f"T={T:.02f}, R={R:.02f}")
