# Recursive Catalan Numbers


def catalan(n):
    if n == 0:
        return 1

    return (4 * n - 2) * catalan(n - 1) / (n + 1)


print(catalan(100))


# (b)
def gcd(m, n):
    if n == 0:
        return m
    return gcd(n, m % n)


print(gcd(108, 192))
