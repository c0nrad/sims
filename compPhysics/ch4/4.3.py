def f(x):
    return x * (x - 1)


def df(x, h):
    return (f(x + h) - f(x)) / h


print(f"df(x=1, h=1e-2)={df(1, 1e-2)}")
print(f"df_real=2x-1")

for h in [1e-4, 1e-6, 1e-8, 1e-10, 1e-12, 1e-14]:
    print(f"df(x=1, h={h})={df(1, h)}")

# It's smaller and then better due to rounding errors