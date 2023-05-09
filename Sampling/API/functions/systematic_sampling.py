from sampleSize import dowellSampleSize
from random import randrange, uniform


def dowellSystematicSampling():
    N = 5
    # n = dowellSampleSize()
    n = 2
    Yi_input = input("Enter the population values(comma separated): ")
    # assumes values are integers
    Yi = [int(i) for i in Yi_input.split(",")]

    # check if N divides n without remainder
    if N % n == 0:
        k = N // n
        i = randrange(0, k)
        # select first unit randomly
        Yi = Yi[i:] + Yi[:i]
        sample_units = [Yi[ind] for ind in range(i, N, k)]
    else:
        k = N / n
        i = round(uniform(0, k))
        if i > N:
            i -= 1
        # select first unit randomly
        Yi = Yi[i:] + Yi[:i]
        k = round(k)
        sample_units = [Yi[ind] for ind in range(i, N, k)]
    return sample_units
a = dowellSystematicSampling()
print(a)
