from bitarray import bitarray
import math

# (a)
def primes_memory(n):
    a = bitarray(n)
    a.setall(1)
    a[0] = 0
    a[1] = 0

    primes = []

    for i in range(2, n):
        if not a[i]:
            continue

        primes.append(i)

        k = 2
        while k * i < n:
            a[k * i] = 0
            k += 1

    return primes


def primes_cpu(n):
    primes = [2]
    for n in range(3, n):
        # print(n)
        is_factor = False
        for p in primes:
            # print(n, p)
            if n % p == 0:
                print(n, p)
                is_factor = True
                break
            if p >= math.sqrt(n):
                break
        if not is_factor:
            primes.append(n)

    return primes


print(primes_memory(10000))
print(primes_cpu(10000))

# Memory is much better
