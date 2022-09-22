import math

x = input("x: ")
y = input("y: ")

x = float(x)
y = float(y)

r = math.sqrt(x ** 2 + y ** 2)
theta = math.atan2(y, x) * 180 / math.pi

print(f"r={r:.02f}, theta={theta:.02f}")
