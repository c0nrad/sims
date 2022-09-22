from ising_1d import Ising1D
import numpy as np
import matplotlib.pyplot as plot

from ising_1d_chains import get_next_spin_probabilistic

N = 5000
grid = Ising1D(N, 3)

correct = []
guess = []

Ts = np.linspace(5, 0.1, 10)
for t in Ts:
    print(t)
    grid.T = t

    avgCorrect = 0
    avgGuess = 0

    iters = 20
    for i in range(iters):
        grid.loop(10000)

        states = grid.count_normalized_states()

        fiveUpCount = 0
        for i in range(N):
            if (
                grid.at(i) == 1
                and grid.at(i + 1) == 1
                and grid.at(i + 2) == 1
                and grid.at(i + 3) == 1
                and grid.at(i + 4) == 1
            ):
                fiveUpCount += 1

        # print("Four Up Count", fiveUpCount)
        # print(states["uuu"] * states["uuu"] / (states["uud"] / 2 + states["uuu"]) * N)

        avgCorrect += fiveUpCount
        avgGuess += (
            states["uuu"]
            * get_next_spin_probabilistic("uu", states)["u"]
            * get_next_spin_probabilistic("uu", states)["u"]
            * N
        )

    correct.append(avgCorrect / iters)
    guess.append(avgGuess / iters)

plot.plot(Ts, correct, label="Correct")
plot.plot(Ts, guess, label="Guess")
plot.legend()
plot.show()
plot.pause(0)
