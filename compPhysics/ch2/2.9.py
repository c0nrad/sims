from math import sqrt

N = 100
v = 0
for i in range(-N, N):
    for j in range(-N, N):
        for k in range(-N, N):
            if i == 0 and j == 0 and k == 0:
                continue

            # print(i, j, k)
            if (i + j + k) % 2 == 0:
                v += 1 / sqrt(i * i + j * j + k * k)
            else:
                v -= 1 / sqrt(i * i + j * j + k * k)

print(f'M={v}')
