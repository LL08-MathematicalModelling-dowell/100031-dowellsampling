from random import randrange

def dowellRandomGeneration(N, n, Yi):
    sampleUnits = []
    try:
        rand_nos = [randrange(0, N) for _ in range(n)]
        sampleUnits = [Yi[i] for i in rand_nos]
    except IndexError:
        return "Error: The specified index is out of range. Please try again increase or decrease the value."
    return sampleUnits
