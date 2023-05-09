
from API.functions.sampleSize import dowellSampleSize

"""
Function to perform systematic sampling on a given population.

Parameters:
Yi (list): List of population units.
N (int): Population size.
n (int): Sample size.
i (int): Random start.
circular (bool): Whether to select samples in a circular manner (default: True).

Returns:
samples (list): List of k unique systematic samples from the population units.
"""

# from sampleSize import dowellSampleSize
import random

def dowellSystematicSampling(Yi, n):
    N = len(Yi)
    # n = 9
    # check if N divides n without remainder
    if N % n == 0:
        k = N // n
        i = random.randint(0, k-1)
        # select first unit randomly
        Yi = Yi[i:] + Yi[:i]
        sample_units = [Yi[ind] for ind in range(0, N, k)]
    else:
        k = N / n
        i = round(random.uniform(0, k))
        if i >= N:
            i -= 1
        # select first unit randomly
        Yi = Yi[i:] + Yi[:i]
        k = round(k)
        sample_units = [Yi[ind] for ind in range(0, N, k)]
    return sample_units

# Yi = [
#     "India", "USA", "China", "Russia", "Germany",
#     "Uttar Pradesh", "Texas", "California", "Georgia", "Florida",
#     "Mumbai", "New York", "Los Angeles", "Chicago", "Berlin",
#     "Delhi", "Washington DC", "San Francisco", "Atlanta", "Hamburg",
#     "Pune", "Houston", "Dallas", "Miami", "Seattle",'Kolkata','Boston','Austin','Orlando','Portland','ranchi','karanchi',
#     'MP','tokyo','fukuka','Mount fuji','Mount everest','Mount k2','Mount kanchenjunga','Mount lhotse','Mount makalu','Mount cho oyu','nagasaki','kyoto',''
# ]
# N = len(Yi)
# e = 0.05 # desired margin of error (5%)
# n = dowellSampleSize(N, e) # calculate sample size
# print(n) 
# i = random.randint(1, N)
# samples = dowellSystematicSampling(Yi, n)
# print(samples)
