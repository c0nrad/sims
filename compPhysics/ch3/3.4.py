from vpython import sphere, vector
import math

L = 2
R = 0.2

# A
# for x in range(-L, L + 1):
#     for y in range(-L, L + 1):
#         for z in range(-L, L + 1):
#             sphere(pos=vector(x, y, z), radius=R, color=vector((x + y + z) % 2, 1, 0))

# B
for x in range(0, L):
    for y in range(0, L):
        for z in range(0, L):

            sphere(pos=vector(x, y, z), radius=R, color=vector(1, 0, 0))

            if x != L - 1 and y != L - 1:
                sphere(pos=vector(x + 0.5, y + 0.5, z), radius=R)

            if y != L - 1 and z != L - 1:
                sphere(pos=vector(x, y + 0.5, z + 0.5), radius=R)

            if x != L - 1 and z != L - 1:
                sphere(pos=vector(x + 0.5, y, z + 0.5), radius=R)
