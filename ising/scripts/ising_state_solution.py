from typing import Dict
from ising_state_vector import IsingStateVector
from ising import Ising
import numpy as np
import random
import math
import matplotlib.pyplot as plot
import grid_builder


def is_valid_state(state):
    return state in [
        "uuuuu",
        "uuuud",
        "uuudd",
        "uudud",
        "uuddd",
        "udddd",
        "ddddd",
        "ddddu",
        "ddduu",
        "ddudu",
        "dduuu",
        "duuuu",
    ]


def filter_zeros(a: Dict[any, float]):
    out = {}
    for k, v in a.items():
        if v != 0:
            out[k] = v
    return out


def opposite_color(color):
    if color == "u":
        return "d"
    elif color == "d":
        return "u"
    else:
        print(color, "color")
        raise Exception("not a valid color")


def normalize_state(state):
    for i in range(4):
        if is_valid_state(state):
            return state
        state = state[0] + state[2:] + state[1]
    raise Exception("unable to nroamlzie state")


def add_probability_to_vector(out: Dict[IsingStateVector, float], vector: IsingStateVector, probability: float):
    for known_vector in out:
        if known_vector == vector:
            out[vector] += probability
            return

    out[vector] = probability


def neighbor_probabilities(states, neighbor_middle, neighbor_edge):
    probabilities = []
    for state in states:
        if state[0] != neighbor_middle or state[1:].count(neighbor_edge) == 0:
            probabilities.append(0)
            continue
        else:
            probabilities.append(states[state])

    if sum(probabilities) == 0:
        raise Exception("no matching states")
    probabilities = np.asarray(probabilities) / sum(probabilities)
    return {list(states.keys())[i]: probabilities[i] for i in range(len(probabilities))}


def flipped_edge_probabilities(state, edge_color):
    if state[1:].count(edge_color) == 0:
        return {}

    out = {}
    total_states = 0
    for d in range(4):
        if state[d + 1] == edge_color:
            new_state = state[0] + state[1 : d + 1] + opposite_color(edge_color) + state[d + 2 :]
            new_state = normalize_state(new_state)
            if new_state not in out:
                out[new_state] = 1
            else:
                out[new_state] += 1
            total_states += 1

    return {state: p / total_states for (state, p) in out.items()}


assert flipped_edge_probabilities("udddd", "d") == {"uuddd": 1}
assert flipped_edge_probabilities("uuddd", "d") == {
    "uuudd": 2 / 3.0,
    "uudud": 1 / 3.0,
}  # xxx: should it really be 2/3, 1/3?


def probability_to_next_states(vector: IsingStateVector, T: float):
    vector = vector.clone()

    out = {}
    i = 0
    # initial_probabilities = vector.state_probabilities(vector.states)
    for state in vector.states:
        p = vector.states[state] / sum(list(vector.states.values()))
        if p == 0:
            continue

        new_vector = vector.clone()

        dE = 0
        dE = sum([1 if s == 'u' else -1 for s in state[1:]])
        dE *= 2 * (1 if state[0] == 'u' else -1)

        # print(state, dE)

        if dE > 0:
            # Probability to do nothing
            add_probability_to_vector(out, vector, p * (1 - math.exp(-dE / T)))
            p = p * math.exp(-dE / T)

        new_vector.states[state] -= 1
        new_vector.states[new_vector.normalize_state(new_vector.flip_middle(state))] += 1

        u_neighbors = filter_zeros(neighbor_probabilities(new_vector.states, state[1], state[0]))
        for u_neighbor in u_neighbors:
            u_vector = new_vector.clone()
            u_vector.states[u_neighbor] -= 1
            r_neighbors = filter_zeros(neighbor_probabilities(u_vector.states, state[2], state[0]))
            for r_neighbor in r_neighbors:
                r_vector = u_vector.clone()
                r_vector.states[r_neighbor] -= 1
                d_neighbors = filter_zeros(neighbor_probabilities(r_vector.states, state[3], state[0]))
                for d_neighbor in d_neighbors:
                    d_vector = r_vector.clone()
                    d_vector.states[d_neighbor] -= 1
                    l_neighbors = filter_zeros(neighbor_probabilities(d_vector.states, state[4], state[0]))
                    for l_neighbor in l_neighbors:
                        l_vector = d_vector.clone()
                        l_vector.states[l_neighbor] -= 1
                        subtracted_vector = l_vector.clone()

                        final_u_neighbors = filter_zeros(flipped_edge_probabilities(u_neighbor, state[0]))
                        final_r_neighbors = filter_zeros(flipped_edge_probabilities(r_neighbor, state[0]))
                        final_d_neighbors = filter_zeros(flipped_edge_probabilities(d_neighbor, state[0]))
                        final_l_neighbors = filter_zeros(flipped_edge_probabilities(l_neighbor, state[0]))

                        for final_u_neighbor in final_u_neighbors:
                            for final_r_neighbor in final_r_neighbors:
                                for final_d_neighbor in final_d_neighbors:
                                    for final_l_neighbor in final_l_neighbors:
                                        final_vector = subtracted_vector.clone()
                                        final_vector.states[final_u_neighbor] += 1
                                        final_vector.states[final_r_neighbor] += 1
                                        final_vector.states[final_d_neighbor] += 1
                                        final_vector.states[final_l_neighbor] += 1

                                        final_p = (
                                            p
                                            * u_neighbors[u_neighbor]
                                            * r_neighbors[r_neighbor]
                                            * d_neighbors[d_neighbor]
                                            * l_neighbors[l_neighbor]
                                            * final_u_neighbors[final_u_neighbor]
                                            * final_r_neighbors[final_r_neighbor]
                                            * final_d_neighbors[final_d_neighbor]
                                            * final_l_neighbors[final_l_neighbor]
                                        )

                                        add_probability_to_vector(out, final_vector, final_p)

    original_total_states = vector.total_states()

    for (vector, p) in out.items():
        if p < 0:
            raise Exception("Negative Probability")

        if vector.total_states() != original_total_states:
            raise Exception("mismatch in total states")

    if (sum(list(out.values())) - 1) > 0.05:
        raise Exception("probabilities do not sum to 1")

    return out


# 2.596


def plot_next_CD():
    print("Critical T", 2 / math.log(1 + math.sqrt(2)))

    gridSize = 10000

    original_model = Ising(gridSize, 2 / math.log(1 + math.sqrt(2)))
    # for x in range(gridSize):
    #     for y in range(gridSize):
    #         if y < gridSize / 2:
    #             original_model.grid[x][y] = 1
    #         else:
    #             original_model.grid[x][y] = -1

    print("GridSize = ", gridSize, "Temp =", original_model.T)
    original_model.loop(1000000000)
    original_vector = IsingStateVector(original_model)
    print(original_vector.states)
    print("original mag", original_model.calculateMagnatism())
    # (C1_original, C2_original) = original_vector.calculate_simple_correlation_function()
    print("original dist function", original_vector.calculate_simple_correlation_function())

    C1 = []
    C2 = []
    Ms = []
    Ts = np.linspace(0.1, 5, 11)
    for t in Ts:
        print(t)

        # 2.26918531421
        next_vector = probability_to_next_states(original_vector, t)
        next_vector = dict(sorted(next_vector.items(), key=lambda item: item[1], reverse=True))

        # print("Original_simple_c", original_C)
        # print("original_long_c", original_C_long)
        # for (vector, p) in list(next_vector.items())[0:10]:
        #     new_c = vector.calculate_simple_correlation_distance()
        #     long_c = vector.calculate_correlation_distance(6)
        #     print(f'p={p}, Dnew_c={original_C - new_c}, Dlong_c={original_C_long - long_c}', vector)
        #     print(f'long_correlation', vector.calculate_correlation_function(3))

        # input()

        # C1_avg = 0
        # C2_avg = 0
        
        for (vector, p) in list(next_vector.items()):
            print(p, vector)
            M_avg += (vector.calculate_simple_correlation_function()[0]) * p
            C2_avg += (vector.calculate_simple_correlation_function()[1]) * p
            print(p, vector)

        # c_avg_old += vector.calculate_correlation_distance(2) * p
        # print("original_mag", original_mag, "new mag", dM)
        # print("original_c", original_C, "new c", c_avg)
        # print("original_c", original_C, "new_c", c_avg)
        # print("long c", c_avg_old)
        C1.append(C1_avg)
        C2.append(C2_avg)

        print("Recent C1, C2", C1[-1], C2[-1])

        # print("down, up", down, up)
        # Cs.append(avg)
        # print("result", t, Cs[-1])

    plot.plot(Ts, C1, label="c1")
    # plot.plot(Ts, C2, label="c2")

    plot.axhline(C1_original)
    # plot.axhline(C2_original)
    plot.legend()

    plot.grid()
    plot.show()
    plot.pause(0)


def weighted_avg_and_std(values, weights):
    """
    Return the weighted average and standard deviation.

    values, weights -- Numpy ndarrays with the same shape.
    """
    average = np.average(values, weights=weights)
    # Fast and numerically precise:
    variance = np.average((values - average) ** 2, weights=weights)
    return (average, math.sqrt(variance))


if __name__ == "__main__":

    plot_next_CD()

    # gridSize = 500
    # original_model = Ising(gridSize, 1)
    # state_model = IsingStateVector(original_model)

    # # 2.26918531421
    # next_vector = probability_to_next_states(state_model, 2.2692)
    # next_vector = dict(sorted(next_vector.items(), key=lambda item: item[1], reverse=True))

    # print(len(set(next_vector.keys())), len(next_vector.keys()))

    # for (vector, p) in list(next_vector.items())[0:20]:
    #     print(f'{p: .05f}:  {vector.calculate_magnetism()} {vector}')

    # m_next = 0
    # for (vector, p) in next_vector.items():
    #     m_next += p * vector.calculate_magnetism()

    # print(f'<M_next> = {m_next}')
