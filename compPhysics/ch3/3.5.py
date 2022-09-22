from vpython import sphere, vector, rate
from numpy import empty
import math

planets = [
    ("Mercury", 2440, 57.9, 88),
    ("Venus", 6052, 108.2, 224.7),
    ("Earth", 6371, 149.6, 365.3),
    ("Mars", 3386, 227.9, 687.0),
    ("Jupiter", 69173, 778.5, 4331.6),
    ("Saturn", 57316, 1433.4, 10759.2),
    # ("Sun", 695500, 0, 0),
]

sizeScale = 1e-4
radiusScale = 1e-1

planet_spheres = empty(len(planets), sphere)
for i in range(len(planets)):
    planet = planets[i]
    planet_spheres[i] = sphere(radius=sizeScale * planet[1], pos=vector(radiusScale * planet[2], 0, 0))

sun = sphere(radius=5, color=vector(1, 0, 0))

for day in range(0, 500):
    rate(30)

    for i in range(len(planets)):
        planet = planets[i]
        T = planet[3]
        radius = planet[2]
        angle = (day % T) / T * 180 / math.pi

        x = math.cos(angle) * radiusScale * radius
        y = math.sin(angle) * radiusScale * radius

        planet_spheres[i].pos = vector(x, y, 0)
