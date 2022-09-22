import math

x = float(input("x (ly): "))
beta = float(input("v/c: "))

gamma = 1 / math.sqrt(1 - beta ** 2)

# I need to play more with relativity, stuff don't make any sense
print(f"As seen by earth: {x/beta:.02f}")
print(f"As seen by spaceship: {x/beta / gamma:.02f}")
