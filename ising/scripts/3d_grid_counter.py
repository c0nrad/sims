from copy import copy
import numpy as np

L = 1


def next_hops(path):
    last_spot = path[-1]

    x, y, z = last_spot
    neighbors = [(x, y + 1, z), (x + 1, y, z), (x, y - 1, z), (x - 1, y, z), (x, y, z + 1), (x, y, z - 1)]
    out = []
    for n in neighbors:
        if n not in path:
            new_path = copy(path)
            new_path.append(n)
            out.append(new_path)

    return out


# assert next_hops([(0, 0), (0, 1)]) == [[(0, 0), (0, 1), (0, 2)], [(0, 0), (0, 1), (1, 1)], [(0, 0), (0, 1), (-1, 1)]]

out = ""
currSum = 0
for max_hops in range(1, 20, 1):
    path_queue = [[(0, 0, 0)]]

    hops = 0
    while hops < max_hops:
        hops += 1
        next_path_queue = []
        for p in path_queue:
            # print("p", p)
            next_paths = next_hops(p)

            for path in next_paths:
                next_path_queue.append(path)
        path_queue = next_path_queue
        # print("hops", hops, path_queue)

    # print("\npath_queue)
    count = sum([1 for p in path_queue if p[-1] == (L, 0, 0)])
    # for path in path_queue:
    #     if path[-1] == (L, 0):
    #         print(path)

    currSum += count * np.tanh(np.log(np.sqrt(2) + 1) / 2) ** max_hops
    if count != 0:
        print(max_hops, count, currSum)
        out += str(count) + "*Tanh[1/t]^" + str(max_hops) + "+ "
        print(out[0:-2])
