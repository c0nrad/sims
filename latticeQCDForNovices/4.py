# bootstrap and bins

import random
import numpy as np
import matplotlib.pyplot as plot

N = 20  # number of timesteps
a = 0.5  # grid size (deltaT)
eps = 1.4  # metropolis shift amount
N_cor = 20  # path corrections
N_cf = 100  # configurations


def S(j, x):
    jp = (j + 1) % N
    jm = (j - 1) % N
    return a * (x[j] ** 2) / 2.0 + x[j] * (x[j] - x[jp] - x[jm]) / a


def metropolis_path_update(x):
    for j in range(0, N):
        x_prev = x[j]
        S_prev = S(j, x)
        x[j] += np.random.uniform(-eps, eps)
        dS = S(j, x) - S_prev
        if dS > 0 and np.exp(-dS) < np.random.uniform(0, 1):
            x[j] = x_prev


def compute_G(x, n):
    g = 0.0
    for j in range(0, N):
        g += x[j] * x[(j + n) % N]
    return g / N


def monte_carlo_average(x, G):

    # Initialize x
    for j in range(0, N):
        x[j] = 0

    # Thermalize x
    for j in range(0, 10 * N_cor):
        metropolis_path_update(x)

    for alpha in range(0, N_cf):
        for j in range(0, N_cor):
            metropolis_path_update(x)

        for n in range(0, N):
            G[alpha][n] = compute_G(x, n)


def calculate_average(G):
    return np.sum(G, axis=0) / len(G)


def calculate_dE(G):
    g = calculate_average(G)
    return np.log(np.abs(g[:-1] / g[1:])) / a


def calculate_standard_deviation(G):
    g = np.asarray(G)
    g_sdev = np.abs(calculate_average(g ** 2) - calculate_average(g) ** 2) ** (1.0 / 2)
    return g_sdev


def bootstrap(G):
    N_cf = len(G)
    G_bootstrap = []
    for i in range(0, N_cf):
        alpha = int(np.random.uniform(0, N_cf))
        G_bootstrap.append(G[alpha])
    return G_bootstrap


def bin(G, binsize):
    G_binned = []
    for i in range(0, len(G), binsize):
        G_avg = 0
        for j in range(0, binsize):
            G_avg = G_avg + G[i + j]
        G_binned.append(G_avg / binsize)
    return G_binned


def bootstrap_dE(G, N_bootstrap=100):
    dE_avg = calculate_dE(G)
    dE_bs = []

    for i in range(N_bootstrap):
        g = bootstrap(G)
        dE_bs.append(calculate_dE(np.asarray(g)))
    dE_sdev = calculate_standard_deviation(np.asarray(dE_bs))

    return (dE_avg, dE_sdev)


x = np.zeros(N)
G = np.zeros((N_cf, N))

monte_carlo_average(x, G)
(dE_avg, dE_sdev) = bootstrap_dE(G, 20)

plot.errorbar([a * x for x in range(0, N - 1)], dE_avg, dE_sdev)
plot.xlabel("t")
plot.ylabel("En+1 - En")
plot.xlim([-0.5, 2.5])
plot.ylim([-1, 3])
plot.show()
plot.pause(0)