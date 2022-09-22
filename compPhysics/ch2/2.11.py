import math

# (a)
def binomial(n, k):
    if k == 0:
        return 1

    return math.factorial(n) / (math.factorial(k) * math.factorial(n - k))


# (b) pascal's triangle
def print_pascals_triangle():
    for n in range(1, 20):
        for k in range(n + 1):
            # print(n, k)
            print(int(binomial(n, k)), end=" ")

        print("")


# (c)
def coin_heads_probability(coins_n, tosses_k):
    return binomial(coins_n, tosses_k) / 2 ** coins_n


print(f"Probability a coin tossed 100 times comes up heads 60 times: {coin_heads_probability(100, 60)*100}%")
print(
    f"Probability a coin tossed 100 times comes up heads 60 times or more: {sum([coin_heads_probability(100, k)*100 for k in range(60, 100)])}%"
)
