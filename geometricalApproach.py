from random import randrange

def dowellGeometricalFunction(N, n, Yi):
    # inscribe the circle randomly by starting from a random index
    start = randrange(0, N)
    Yi = Yi[start:] + Yi[:start]
    # partition the population list into 3 parts corresponding to the areas
    # where the triangle touches the circle x, y and z are the three regions
    # in which the triangle will rotate
    partition = N // 3
    x, y, z = (
        Yi[:partition],
        Yi[partition : (2 * partition)],
        Yi[(2 * partition) :],
    )
    # check if lists x, y, and z have at least one element
    if len(x) > 0 and len(y) > 0 and len(z) > 0:
        sampleUnits = []
        for _ in range(n // 3):
            # check if indices are within the bounds of the lists
            if len(x) > 0 and len(y) > 0 and len(z) > 0:
                sampleUnits.append([x[0], y[0], z[0]])
                # rotate by 1 value
                x = x[1:] + x[:1]
                y = y[1:] + y[:1]
                z = x[1:] + z[:1]
            else:
                return []  # or handle the error condition as per your requirements
        return sampleUnits
    else:
        return "Please decrease or increase the value of 'N' to ensure at least 3 units in each partition."
