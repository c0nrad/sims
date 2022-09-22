def d1(n):
    return n * (n + 1)


def d2(n):
    return (1 / 4) * (n) * (3 + n) * (6 - n + n ** 2)


print([d2(n) for n in range(10)])
