from copy import deepcopy
from ising import Ising, count_states
import numpy as np
import random
import math
from scipy.optimize import curve_fit
import matplotlib.pyplot as plot
import json
import sympy

from utils import ud_to_value


class IsingStateVector:
    def __init__(self, model):
        if model != None:
            # print(model)
            self.states = self.count_states(model)
        else:
            out = {}
            out["uuuuu"] = 0
            out["uuuud"] = 0
            out["uuudd"] = 0
            out["uudud"] = 0
            out["uuddd"] = 0
            out["udddd"] = 0

            out["ddddd"] = 0
            out["ddddu"] = 0
            out["ddduu"] = 0
            out["ddudu"] = 0
            out["dduuu"] = 0
            out["duuuu"] = 0
            self.states = out

    def from_states(states):
        out = IsingStateVector(None)
        out.states = states
        return out

    def count_states(self, model):
        out = {}

        out["uuuuu"] = 0
        out["uuuud"] = 0
        out["uuudd"] = 0
        out["uudud"] = 0
        out["uuddd"] = 0
        out["udddd"] = 0

        out["ddddd"] = 0
        out["ddddu"] = 0
        out["ddduu"] = 0
        out["ddudu"] = 0
        out["dduuu"] = 0
        out["duuuu"] = 0

        for x in range(0, model.gridSize):
            for y in range(0, model.gridSize):
                middle = 'u' if model.at(x, y) == 1 else 'd'
                border = (model.at(x, y - 1), model.at(x + 1, y), model.at(x, y + 1), model.at(x - 1, y))
                border = "".join(['u' if a == 1 else 'd' for a in border])

                while middle + border not in out:
                    border = border[1:] + border[0]

                out[middle + border] += 1

        return out

    def normalize_probabilities(self):
        total_states = sum(self.states.values())
        for state in self.states:
            self.states[state] /= total_states

    def state_probabilities(self):
        total_states = sum(self.states.values())

        return np.asarray(list(self.states.values())) / total_states

    def calculate_magnetism(self):
        out = 0
        total_states = 0
        for state in self.states:
            if state[0] == 'u':
                out += self.states[state]
            else:
                out -= self.states[state]
            # out += self.states[state] * 1 if state[0] == 'u' else -1
            # out -= self.states[state] * state.count('d') / 5
            total_states += self.states[state]
        return out / total_states

    def calculate_energy_per_spin(self):
        out = 0
        total_states = 0
        for state in self.states:
            middle = ud_to_value(state[0])
            energy = sum([middle * ud_to_value(s) for s in state[1:]])
            out += energy * self.states[state]

            total_states += self.states[state]
        return out / total_states

    def calculate_shannon_entropy(self):
        total_p = sum(self.states.values())
        p = {k: v / total_p for (k, v) in self.states.items()}
        return -sum([p[state] * math.log(p[state]) for state in p if p[state] != 0])

    def calculate_total_magnetism(self):
        out = 0
        for state in self.states:
            if state[0] == 'u':
                out += self.states[state]
            else:
                out -= self.states[state]
            # out += self.states[state] * 1 if state[0] == 'u' else -1
            # out -= self.states[state] * state.count('d') / 5
        return out

    def calculate_correlation_function(self, length=0):

        if length == 0:
            gridSize = math.sqrt(sum(list(self.states.values())))
            length = int(gridSize // 2 - 1)

        link_probabilities = {"uuu": 0, "uud": 0, "udu": 0, "udd": 0, "duu": 0, "dud": 0, "ddu": 0, "ddd": 0}
        total_links = 0

        for state in self.states:
            link_probabilities[state[1] + state[0] + state[3]] += self.states[state]
            link_probabilities[state[2] + state[0] + state[4]] += self.states[state]
            link_probabilities[state[3] + state[0] + state[1]] += self.states[state]
            link_probabilities[state[4] + state[0] + state[2]] += self.states[state]
            total_links += 4 * self.states[state]
        link_probabilities = {k: v / total_links for (k, v) in link_probabilities.items()}
        # print("total links", total_links)

        # print(link_probabilities)

        queue = [([k], v) for (k, v) in link_probabilities.items()]
        r = 0
        for r in range(1, length):
            next_queue = []

            # print(r, queue)
            # print(sum([o[1] for o in queue]))
            for (path, probability) in queue:
                u_path = path[-1][1] + path[-1][2] + "u"
                d_path = path[-1][1] + path[-1][2] + "d"
                total_p = link_probabilities[u_path] + link_probabilities[d_path]
                if total_p != 0:
                    next_queue.append((path + [u_path], probability * (link_probabilities[u_path] / total_p)))
                    next_queue.append((path + [d_path], probability * (link_probabilities[d_path] / total_p)))
                else:
                    next_queue.append((path + [u_path], 0))
                    next_queue.append((path + [d_path], 0))

            queue = next_queue.copy()

        # collapse chains
        chains = []
        for (path, probability) in queue:
            chains.append(("".join([a[0] for a in path]), probability))

        # print(chains)

        out = np.zeros(length)
        for (chain, probability) in chains:
            # print(probability)
            for r in range(1, length):
                if chain[0] == chain[r]:
                    out[r] += probability
                else:
                    out[r] -= probability

        out = out[1:]
        return np.abs(out - self.calculate_magnetism() ** 2)

    def calculate_correlation_distance(self, length=0):
        def exponential_fit(x, g):
            return np.exp(-((x + 1) / g)) / ((x + 1) ** (1 / 4))

        if length == 0:
            gridSize = math.sqrt(sum(list(self.states.values())))
            length = int(gridSize // 2 - 1)

        return curve_fit(
            exponential_fit,
            list(range(length - 1)),
            self.calculate_correlation_function(length),
            # p0=[3, 1],
            # bounds=[[0, 0], [50, 1]],
        )[0][0]

    def total_states(self):
        return sum(list(self.states.values()))

    def normalize_probabilities(self):
        total = self.total_states()
        for key in self.states:
            self.states[key] /= total

    def calculate_simple_correlation_distance(self):
        sisj1 = 0
        sisj2 = 0
        si = 0
        total_states = sum(list(self.states.values()))
        for state in self.states:
            si += self.states[state] * ud_to_value(state[0])

            sisj1 += self.states[state] * (
                ud_to_value(state[0])
                * (ud_to_value(state[1]) + ud_to_value(state[2]) + ud_to_value(state[3]) + ud_to_value(state[4]))
                / 4.0
            )
            sisj2 += (
                self.states[state]
                * ((ud_to_value(state[1]) * ud_to_value(state[3])) + (ud_to_value(state[2]) * ud_to_value(state[4])))
                / 2.0
            )
        # si /= total_states
        # sisj1 /= total_states
        # sisj2 /= total_states

        c1 = sisj1 - (si ** 2)
        c2 = sisj2 - (si ** 2)

        # print(c1, c2)

        return 1 / sympy.log(sympy.sqrt(2) * c1 / c2)

    def calculate_simple_correlation_function(self):
        sisj1 = 0
        sisj2 = 0
        si = 0
        total_states = sum(list(self.states.values()))
        for state in self.states:
            si += self.states[state] * ud_to_value(state[0])

            sisj1 += self.states[state] * (
                ud_to_value(state[0])
                * (ud_to_value(state[1]) + ud_to_value(state[2]) + ud_to_value(state[3]) + ud_to_value(state[4]))
                / 4.0
            )
            sisj2 += (
                self.states[state]
                * ((ud_to_value(state[1]) * ud_to_value(state[3])) + (ud_to_value(state[2]) * ud_to_value(state[4])))
                / 2.0
            )
        si /= total_states
        sisj1 /= total_states
        sisj2 /= total_states

        c1 = sisj1 - (si ** 2)
        c2 = sisj2 - (si ** 2)
        return (c1, c2)

    def loop(self, steps, T):
        for i in range(steps):
            self.step(T)

    def step(self, T):
        total_state_probabilities = self.state_probabilities(self.states)

        # Pick a random state
        state = np.random.choice(list(self.states.keys()), p=total_state_probabilities)

        # Do we flip it?
        dE = 0
        dE = sum([1 if s == 'u' else -1 for s in state[1:]])
        dE *= 2 * (1 if state[0] == 'u' else -1)

        if not (dE <= 0 or random.random() < math.exp(-dE / T)):
            return

        # Do center flip
        self.states[state] -= 1
        self.states[self.normalize_state(self.flip_middle(state))] += 1

        neighbors = []
        skipNeighbors = [False, False, False, False]
        # Claim Neighbors
        for edge in range(4):
            try:
                neighbor = self.pick_random_state(state[edge + 1], state[0])
                neighbors.append(neighbor)
                self.states[neighbor] -= 1
            except:
                skipNeighbors[edge] = True
                neighbors.append("")

        # Flip Neighbors
        for n in range(4):
            if not skipNeighbors[n]:
                self.states[self.flip_random_edge_and_normalize(neighbors[n], state[0])] += 1

        return

    def flip_random_edge_and_normalize(self, state, color):
        if state[1:].count(color) == 0:
            print(state, color)
            raise Exception("state does not have color!")

        d = np.random.choice([0, 1, 2, 3])
        while True:
            if state[d + 1] == color:
                break
            d = np.random.choice([0, 1, 2, 3])

        new_state = state[0] + state[1 : d + 1] + self.opposite_color(color) + state[d + 2 :]
        new_state = self.normalize_state(new_state)

        return new_state

    def normalize_state(self, state):
        for i in range(4):
            if state in self.states:
                return state
            state = state[0] + state[2:] + state[1]
        raise Exception("unable to nroamlzie state")

    def pick_random_state(self, middle, edge):
        probabilities = []
        for state in self.states:
            if state[0] != middle or state[1:].count(edge) == 0:
                probabilities.append(0)
                continue
            else:
                probabilities.append(self.states[state])

        if sum(probabilities) == 0:
            raise Exception("no matching states")
        probabilities = np.asarray(probabilities) / sum(probabilities)
        return np.random.choice(list(self.states.keys()), p=probabilities)

    def flip_middle(self, state):
        if state[0] == 'u':
            return 'd' + state[1:]
        elif state[0] == 'd':
            return 'u' + state[1:]
        else:
            print(state[0], "color")
            raise Exception("not a valid color")

    def opposite_color(self, color):
        if color == "u":
            return "d"
        elif color == "d":
            return "u"
        else:
            print(color, "color")
            raise Exception("not a valid color")

    def print_state_distribution(self):

        plot.plot(self.states.keys(), self.states.values())

        plot.legend(loc="upper right")
        plot.show()
        plot.pause(0)
        # count_states(model)

    def clone(self):
        out = IsingStateVector(None)
        out.states = deepcopy(self.states)
        return out

    def __eq__(self, other):
        if type(other) is not type(self):
            return False

        if len(self.states) != len(other.states):
            return False

        for state in self.states:
            if self.states[state] != other.states[state]:
                return False

        return True

    def __hash__(self):
        # print(hash(json.dumps(self.states)))
        return hash(json.dumps(self.states))

    def __str__(self):
        return json.dumps(self.states)

    def __repr__(self):
        return json.dumps(self.states)


def is_normalized_state(state):

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


def normalize_state(state):
    for i in range(4):
        if is_normalized_state(state):
            return state
        state = state[0] + state[2:] + state[1]
    raise Exception("unable to nroamlzie state")


# def test_clone():
# i = IsingStateVector(Ising(3, 1))
# i2 = i.clone()
# i.states["uuuuu"] += 1
# assert i.states['uuuuu'] != i2.states['uuuuu']


if __name__ == "__main__":
    gridSize = 20
    original_model = Ising(gridSize, 2 / math.log(math.sqrt(2) + 1))
    print("here")
    original_model.loop(10000000)
    print("after")
    # original_model.grid = np.ones((gridSize, gridSize))
    state_model = IsingStateVector(original_model)

    state_model.print_state_distribution()
    # state_model.loop(50000, 0.1)

    # Ts = np.linspace(2.1, 2.4, 11)
    # Ms = []
    # Cds = []
    # Cfs = []
    # States = []
    # for t in Ts:
    #     print("----")
    #     print("T=", t)
    #     state_model.loop(1000000000, t)

    #     Ms.append(state_model.calculate_magnetism())
    #     print("<M>=", state_model.calculate_magnetism())

    #     States.append(state_model.states.copy())
    #     print("States", state_model.states)
    #     print("sum", sum(list(state_model.states.values())))

    #     Cds.append(state_model.calculate_simple_correlation_distance())

    #     # Cfs.append(state_model.calculate_correlation_function())
    #     # print("Correlation_function", state_model.calculate_correlation_function())
    #     # print("correlation_distance", state_model.calculate_correlation_distance())
    #     # print(s

    # fig, axs = plot.subplots(2, 2)
    # axs[0, 0].plot(Ts, Ms)
    # axs[0, 0].set_title('<M>')
    # # axs[0, 1].plot(Ts, States)
    # # axs[0, 1].set_title('States')
    # axs[1, 0].plot(Ts, Cds)
    # axs[1, 0].set_title('Correlation Distances')
    # # axs[1, 1].plot(Ts, Cfs)
    # # # axs[1, 1].set_title('Correlation Functions')

    # plot.show()
    # plot.pause(0)

    # # # while True:
    # # i.step()
    # # i.dump()
    # # print("<M>", i.calculateMagnatism())
    # # print("Correlation Distance", i.calculateCorrelationFunction())
    # # iv = IsingStateVector(i)
    # # print(iv.states)
    # # print("<M_iv>", iv.calculate_magnetism())
    # # print("Correlation Dist iv:", iv.calculate_correlation_function2(10))

    # # i.loop(100000)
    # # print("Official magnetistm after running:", i.calculateMagnatism())
    # # print(IsingStateVector(i).states)

    # # # for j in range(10000):
    # # #     iv.step(2.27)

    # # while True:
    # #     print("Running 100000")
    # #     # print("st=", t)
    # #     for j in range(100000):
    # #         iv.step(temp)

    # #     i.T = temp
    # #     i.loop(100000)
    # #     print("original ising magnestim: ", i.calculateMagnatism())
    # #     print("After 100000 steps of iv, magenstism", iv.calculate_magnetism())
    # #     print(iv.states)

    # #     input()
