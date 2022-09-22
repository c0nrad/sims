def reducer(reduced):
    while len(reduced) != 1:
        print(reduced)
        new_reduced = []
        for i in range(len(reduced) - 1):
            new_reduced.append(reduced[i + 1] - reduced[i])
        reduced = new_reduced
        # print(reduced)


reduced1 = [2, 6, 12, 20, 30, 42, 56, 72, 90, 110, 132]
reduced2 = [0, 6, 20, 54, 126, 260, 486, 840, 1364]
reduced3 = [28, 92, 256, 654, 1552, 3428, 7072, 13706, 25124]

# c1 = [2, 6, 28, 140, 744, 4166, 23504]

reducer(reduced2)
