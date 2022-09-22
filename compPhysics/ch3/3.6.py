import numpy as np
import matplotlib.pyplot as plot

initial_x = 0.5
iterations = 1000

r = np.linspace(1, 4, 300 + 1)
x = np.full(len(r), initial_x)

for i in range(iterations):
    x = r * x * (1 - x)

plot.scatter(r, x)
plot.show()

# a)
# Fixed point doesn't change at all
# Limit cycles will go through a cycle so we'd need multiple plots

# b)
# Near 3.5
