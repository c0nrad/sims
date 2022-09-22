from numpy import loadtxt
from matplotlib.pyplot import plot, show

data = loadtxt('sunspots.txt', float)
months = data[:, 0]
sunspots = data[:, 1]

# plot(months, sunspots)
# show()

# plot(data[:1000, 0], data[:1000, 1])
# show()

plot(data[:1000, 0], data[:1000, 1])
r = 5
avg = []
for k in range(1000):
    y = 1 / (11)
    temp = 0
    for m in range(-r, r):
        if m + k < 0:
            continue

        temp += sunspots[m + k]
    avg.append(temp / 11)
plot(months[:1000], avg)
show()
