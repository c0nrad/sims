import matplotlib.pyplot as plot
from ising import Ising
from ising_state_vector import IsingStateVector
import numpy as np
from pprint import pprint
from ising_detailed_balance_pairs import (
    calculate_diagonal_pair_probability,
    enumerate_all_diagonal_pairs,
)


def count_diagonal_pair_occurances(model: Ising, middle_state, top_right_state):
    count = 0

    for x in range(model.gridSize):
        for y in range(model.gridSize):
            if model.state_at(x, y) == middle_state and model.state_at(x + 1, y - 1) == top_right_state:
                count += 1

    return count


# assert count_pair_occurances(ones_grid(3), "uuuuu", "uuuuu") == 9
# assert count_pair_occurances(ones_grid(3), "uuuuu", "uuuud") == 0


N = 80

if __name__ == "__main__":
    original_model = Ising(N, 2.6)
    # original_model.grid = np.ones((N, N), dtype=np.int64)
    # original_model.prevEnergy = original_model.calculateEnergy()
    original_model.loop(1000000)
    movesets = enumerate_all_diagonal_pairs()

    moveset_index = 0

    final_probabilities = []
    final_counts = []
    Ts = np.linspace(2.5, 2.6, 10)

    for t in Ts:
        original_model.T = t

        iterations = 10
        # final_probabilities = 0
        # final_counts = 0

        for i in range(iterations):

            original_model.loop(100000)

            before = IsingStateVector(original_model)

            average_counts = 0
            average_probabilities = 0

            # for moveset in [[("ddddd", "uuudd"), ()]]:
            for moveset in [("uuuuu", "uuuuu"), ("ddddd", "ddddd")]:
                probability_of_move_occuring = calculate_diagonal_pair_probability(before, moveset)
                probability_of_move_occuring = probability_of_move_occuring[0] / probability_of_move_occuring[1]
                counts = count_diagonal_pair_occurances(original_model, moveset[0], moveset[1])
                average_probabilities += probability_of_move_occuring
                average_counts += counts

        final_probabilities.append(average_probabilities / iterations)
        final_counts.append(average_counts / iterations)

        print("t, m, probs, counts", t, original_model.calculateMagnatism(), final_probabilities[-1], final_counts[-1])

    plot.plot(Ts, final_probabilities, label="probabilities")
    plot.plot(Ts, final_counts, label="counts")
    plot.legend()
    plot.show()
    plot.pause(0)

    exit(0)
