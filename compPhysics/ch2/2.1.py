from math import sqrt

a = 9.8
h = input("Height of tower (meteres): ")
h = float(h)

# x_f = x_i + v_i + t + .5 * a * t^2
t = sqrt(2 * h / a)

print(f'It will take the ball {t :.2f}s to reach the ground.')