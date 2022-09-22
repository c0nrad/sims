from ising import Ising
import numpy as np
import matplotlib.pyplot as plot
import math

gridSize = 200
Ts = np.linspace(2.1, 2.4, 21)
Xs = []
Xerr = []

i = Ising(gridSize, Ts[0])
i.loop(1000000000)


for t in Ts:
    print(t)
    i.T = t
    i.loop(1000000000)

    # i = Ising(gridSize, t)
    # i.loop(1000000)

    Ms = []
    Ms.append(i.calculateMagnatism())

    for sample in range(100000):
        i.loop(1)
        Ms.append(i.calculateMagnatism())

    print(np.mean(Ms), np.std(Ms))
    var = np.var(Ms)
    Xs.append(var / t / gridSize ** 2)
    print("Xs", Xs[-1])


plot.plot(Ts, Xs)
# plt.errorbar(x, y, e, linestyle='None', marker='^')

plot.grid()
plot.vlines(2 / math.log(1 + math.sqrt(2)), 0, 1e-7)
plot.show()
plot.pause(0)