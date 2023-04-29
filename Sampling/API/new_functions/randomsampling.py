import random
# Dowell's random sampling method
def dowellrandomsampling(stratum, ni):
    sample = []

    # Check that ni is not larger than the population size of the stratum and ni is not negative
    if ni > sum(stratum):
        ni = sum(stratum)
    elif ni < 0:
        ni = 0

    # Sample ni units from stratum without replacement
    if ni > 0:
        sample = random.sample(stratum, ni)

    return sample