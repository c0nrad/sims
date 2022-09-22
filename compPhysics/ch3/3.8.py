import numpy as np
import matplotlib.pyplot as plot


def least_squares(xs, ys):
    Ex = Ey = Exx = Exy = 0
    N = len(xs)

    for i in range(N):
        Ex += xs[i]
        Ey += ys[i]
        Exx += xs[i] ** 2
        Exy += xs[i] * ys[i]

    Ex /= N
    Ey /= N
    Exx /= N
    Exy /= N

    m = (Exy - (Ex * Ey)) / (Exx - Ex ** 2)
    c = (Exx * Ey - Ex * Exy) / (Exx - Ex ** 2)
    return (m, c)


data = np.loadtxt('./millikan.txt')

freqencies = data[:, 0]
voltages = data[:, 1]

(m, c) = least_squares(freqencies, voltages)
print(f'm={m}, c={c}')

bestfit_x = np.linspace(freqencies[0], freqencies[-1], 50)
bestfit_y = m * bestfit_x + c

print(f"h = {m*1.602e-19}")

plot.scatter(freqencies, voltages)
plot.plot(bestfit_x, bestfit_y)

plot.show()
plot.pause(0)
