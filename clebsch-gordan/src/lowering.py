# def lower_eigenvalue(s, m):
#     return (s * (s + 1)) - (m * (m - 1))


s1 = 1.5
s2 = 1

m1 = 0.5
m2 = 0


def total_states(s1, s2):
    return (2 * s1 + 1) * (2 * s2 + 1)


# print("Total States", total_states(s1, s2))

# print(lower_eigenvalue(2.5, 0.5))
# print(lower_eigenvalue(1.5, 0.5))
# print(lower_eigenvalue(0.5, 0.5))


# print(lower_eigenvalue(3 / 2, 0.5))
# print(lower_eigenvalue(1 / 2, 0.5))
import math


def lower_eigenvalue(s, m):
    return math.sqrt(s * (s + 1) - m * (m - 1))


print("| 5/2 5/2> = |3/2 3/2> |1 1>")
print(
    # lower_eigenvalue(2.5, 2.5),
    "|5/2 3/2> = ",
    lower_eigenvalue(1.5, 1.5) / lower_eigenvalue(2.5, 2.5),
    "|3/2 1/2>|1 1> + ",
    lower_eigenvalue(1, 1) / lower_eigenvalue(2.5, 2.5),
    "|1 0>|3/2 3/2>",
)