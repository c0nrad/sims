current = 1
previous = 1
step = 0

while current < 1e9:
    current = (4 * step + 2) / (step + 2) * previous
    print(current)
    previous = current
    step += 1
