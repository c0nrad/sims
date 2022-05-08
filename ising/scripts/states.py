from time import sleep, time
from ising import Ising
import numpy as np
import matplotlib.pyplot as plot


def is_rotate_equal(a, b):
    l = len(a)
    for offset in range(len(a)):
        equal = True
        for j in range(len(a)):
            if a[(offset + j) % l] != b[j]:
                equal = False
                break

        if equal:
            return True
    return False


assert is_rotate_equal([1, 1, 1, 1], [1, 1, 1, 1])
assert is_rotate_equal([0, 1, 1, 1], [1, 0, 1, 1])
assert not is_rotate_equal([1, 0, 1, 0], [1, 1, 1, 0])


def count_states(model: Ising):
    out = {}
    out["1111"] = 0
    out["1110"] = 0
    out["1100"] = 0
    out["1010"] = 0
    out["1000"] = 0
    out["0000"] = 0

    for x in range(0, model.gridSize):
        for y in range(0, model.gridSize):
            state = (model.at(x, y - 1), model.at(x + 1, y), model.at(x, y + 1), model.at(x - 1, y))
            state = [1 if model.at(x, y) == a else 0 for a in state]

            if is_rotate_equal(state, [1, 1, 1, 1]):
                out["1111"] += 1
            elif is_rotate_equal(state, [1, 1, 1, 0]):
                out["1110"] += 1
            elif is_rotate_equal(state, [1, 1, 0, 0]):
                out["1100"] += 1
            elif is_rotate_equal(state, [1, 0, 1, 0]):
                out["1010"] += 1
            elif is_rotate_equal(state, [1, 0, 0, 0]):
                out["1000"] += 1
            elif is_rotate_equal(state, [0, 0, 0, 0]):
                out["0000"] += 1
            else:
                print("Not possible", state)
                exit(0)

    # normalize?
    for k in out:
        out[k] /= model.gridSize * model.gridSize
        out[k] = int(out[k] * 100)

    return out


def print_state_distribution():
    for t in np.linspace(2.5, 2.8, 10):
        t = 2 / np.log(1 + np.sqrt(2))
        print(t)
        model = Ising(100, t)
        model.loop(30000000)
        # model.plot()
        # plot.pause(0)

        states = count_states(model)
        plot.plot(states.keys(), states.values(), label=f"T={t:.02f}")

    plot.legend(loc="upper right")
    plot.show()
    plot.pause(0)
    # count_states(model)


# model = Ising(10, 2)
print_state_distribution()

# while True:
#     print(count_states(model))
#     model.plot()

#     model.step()
#     sleep(2)