import numpy as np
import matplotlib.pyplot as plot

data = np.loadtxt('./velocities.txt')

ts = data[:, 0]  # s
vs = data[:, 1]  # m/s


def integrate_trapezoidal(vs):
    out = 0.5 * vs[0] + 0.5 * vs[-1]
    for k in range(1, len(vs)):
        out += vs[k]

    return out


xs = np.full(len(ts), 0)

for i in range(1, len(ts)):
    print(vs[0:i])
    xs[i] = integrate_trapezoidal(vs[0:i])

plot.plot(ts, vs)
plot.plot(ts, xs)
plot.plot(ts, np.full(len(ts), 0))

plot.show()
plot.pause(0)
