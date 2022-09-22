from copy import copy


# L = 2


def next_hops(path):
    last_spot = path[-1]

    x, y = last_spot
    neighbors = [(x, y + 1), (x + 1, y), (x, y - 1), (x - 1, y)]
    out = []
    for n in neighbors:
        if n not in path:
            new_path = copy(path)
            new_path.append(n)
            out.append(new_path)

    return out


# assert next_hops([(0, 0), (0, 1)]) == [[(0, 0), (0, 1), (0, 2)], [(0, 0), (0, 1), (1, 1)], [(0, 0), (0, 1), (-1, 1)]]

for L in range(2, 3):
    print("L=", L)
    out = ""
    for max_hops in range(1, 20, 1):
        path_queue = [[(0, 0)]]

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
        count = sum([1 for p in path_queue if p[-1] == (L, 0)])
        # for path in path_queue:
        #     if path[-1] == (L, 0):
        #         print(path)

        if count != 0:
            print(max_hops, count)
            out += str(count) + "*Tanh[b]^" + str(max_hops) + "+ "
            print(out[0:-2])
