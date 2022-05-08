from ising import Ising
import matplotlib.pyplot as plot
import numpy as np
from scipy.optimize import curve_fit


def exponential_fit(x, g, a):
    return a * np.exp(-((x) / g))


gridSize = 50
Ts = np.linspace(1.5, 3.5, 20)

N = 30
data = {}

for t in Ts:
    print(t)
    for n in range(N):
        i = Ising(gridSize, t)
        i.loop(5000000)

        # plot.imshow(i.grid)
        # plot.show()
        # i.plot()
        # i.plot()

        c = i.calculateCorrelationFunction()
        # print(c)
        out = 0
        if c[1] == 0:
            out = 0
        else:
            out = curve_fit(exponential_fit, range(gridSize // 2 - 1), c)[0][0]

        if t not in data:
            data[t] = [out]
        else:
            data[t].append(out)
    # plot.plot(range(gridSize // 2 - 1), c, label=f"T={t:.02f}")

# data = np.sum(data, axis=0)

Ts = []
Cs = []
print(data)
for t in data:
    cs = data[t]
    Ts.append(t)

    Cs.append(np.sum(cs) / N)


print(Ts, Cs)

plot.clf()
plot.plot(Ts, Cs)
# plot.legend(loc="upper right")
plot.xlabel("T")
plot.ylabel("Correlation Distance")
plot.show()
plot.pause(0)
