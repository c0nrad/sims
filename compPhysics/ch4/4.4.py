import math

N = 1000000
L = 2
h = L / N

I = 0

for i in range(N):
    x = -1 + (h * i)
    y = math.sqrt(1 - x ** 2)

    I += h * y

print((math.pi / 2 - I) / (math.pi / 2) * 100)
