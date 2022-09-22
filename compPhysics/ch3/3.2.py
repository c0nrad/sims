from numpy import linspace, cos, sin
from matplotlib.pyplot import plot, show
import math

# (a)
theta = linspace(0, 2 * math.pi, 100)

x = 2 * cos(theta) + cos(2 * theta)
y = 2 * sin(theta) - sin(2 * theta)

# plot(x, y)
# show()

# (b) Galilean Spiral

x = []
y = []
for theta in linspace(0, 10 * math.pi):
    r = theta * theta
    x.append(r * cos(theta))
    y.append(r * sin(theta))

# plot(x, y)
# show()


# (c) Fey's Function
x = []
y = []
for theta in linspace(0, 24 * math.pi, 10000):
    r = math.exp(cos(theta)) - 2 * cos(4 * theta) + sin(theta / 12) ** 5
    x.append(r * cos(theta))
    y.append(r * sin(theta))

plot(x, y)
show()
