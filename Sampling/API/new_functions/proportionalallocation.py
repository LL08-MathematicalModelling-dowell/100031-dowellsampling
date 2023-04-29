import random
import time

# Dowell's proportional allocation method
def dowellproportional_allocation(stratum, ni):
    # Calculate total population size and stratum size
    N = sum(stratum)
    n = len(stratum)

    # Calculate allocation probabilities
    p = [x / N for x in stratum]

    # Allocate sample units proportional to stratum size
    sample = [int(round(ni * x)) for x in p]

    # Adjust allocation to account for rounding errors
    while sum(sample) < ni:
        for i in range(n):
            sample[i] += 1
            if sum(sample) == ni:
                break

    return sample
