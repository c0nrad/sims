import numpy as np
import matplotlib.pyplot as plot
from ising import Ising
from ising_state_vector import IsingStateVector

from ising_1d_chains import get_next_spin_probabilistic

N = 20
grid = Ising(N, 1)
correct = []
guess = []

Ts = np.linspace(5, 0.1, 20)
for t in Ts:
    print(t)
    grid.T = t

    avgCorrect = 0
    avgGuess = 0

    iters = 10
    for i in range(iters):
        grid.loop(100000)

        states = IsingStateVector(grid).states
        # states = states.states

        count = 0
        for row in range(N):
            for i in range(N):
                if (
                    grid.at(row, i) == 1
                    and grid.at(row, i + 1) == 1
                    and grid.at(row, i + 2) == 1
                    # and grid.at(row, i + 3) == 1
                    # and grid.at(row, i + 4) == 1
                ):
                    count += 1

        # print("Four Up Count", fiveUpCount)
        # print(states["uuu"] * states["uuu"] / (states["uud"] / 2 + states["uuu"]) * N)

        p_uuu = states["uuuuu"] + states["uuuud"] / 2 + states["uudud"] / 2
        p_uud = (states["uuuud"] / 4) + (states["uuudd"] / 2) + (states["uuddd"] / 4)
        p_dud = states["udddd"] + states["uuddd"] / 2 + states["uudud"] / 2

        # print(p_uuu + 2 * p_uud + p_dud)

        # p_uuuu = p_uuu * (p_uuu) / (p_uuu + p_uud)

        # line_b = states[""]
        # print("Equal?", fiveUpCount, p_uuu * (p_uuu / (p_uuu + (2 * p_uud) + p_dud)))

        # p_next_up = (p_uuu / (p_uuu + (2 * p_uud) + p_dud))

        avgCorrect += count
        avgGuess += p_uuu

    correct.append(avgCorrect / iters)
    guess.append(avgGuess / iters)
    print(correct, guess)

plot.plot(Ts, correct, label="Correct")
plot.plot(Ts, guess, label="Guess")
plot.legend()
plot.show()
plot.pause(0)
