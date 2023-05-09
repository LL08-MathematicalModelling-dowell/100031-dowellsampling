import random

def dowell_stratified_sampling_proportional(Yi, N, n, k, Ni, ni):
    """
    Performs stratified sampling using proportional allocation method.

    Args:
    - Yi: list of population units (strata)
    - N: total population size
    - n: desired sample size
    - k: number of strata
    - Ni: list of stratum sizes
    - ni: list of desired stratum sample sizes

    Returns:
    - sample: list of sampled units
    """
    sample = []
    for i in range(k):
        # Calculate proportional allocation for each stratum
        pi = ni[i] / Ni[i]
        # Randomly sample from stratum based on proportional allocation
        stratum_sample = random.sample(Yi[i], round(Ni[i] * pi))
        sample.extend(stratum_sample)
    # If sample size is not met, randomly sample from population
    if len(sample) < n:
        remaining_sample_size = n - len(sample)
        population_sample = random.sample(Yi, remaining_sample_size)
        sample.extend(population_sample)
    return sample

import math

def dowell_sample_size(N, k, Ni, margin_of_error, confidence_level):
    z = 1.96  # Z-score for 95% confidence level
    p_values = [Ni[i]/N for i in range(k)]
    if 0 in p_values:
        print("Skipping strata with zero population size")
        k = sum(1 for p in p_values if p > 0)
        Ni = [Ni[i] for i in range(k) if p_values[i] > 0]
        p_values = [Ni[i]/N for i in range(k)]
    n = sum([Ni[i]*z**2*p_values[i]*(1-p_values[i])/((Ni[i]-1)*margin_of_error**2+z**2*p_values[i]*(1-p_values[i])) for i in range(k)])
    return math.ceil(n)

# Example usage:
# Example input
Yi = [["India", "Germany"], ["Uttar Pradesh", "Lucknow"], ["Pune", "Munich"]]
N = 600
k = 3
Ni = [2, 2, 2]
margin_of_error = 0.05
confidence_level = 0.95

# Calculate sample size using the dowell_sample_size() function
n = dowell_sample_size(N, k, Ni, margin_of_error, confidence_level)

# Perform stratified sampling using the dowell_stratified_sampling_proportional() function
sample = dowell_stratified_sampling_proportional(Yi, N, n, k, Ni, [1, 1, 1])

# Print sampled units
print(dowell_sample_size(N, k, Ni, margin_of_error, confidence_level))
print(sample)
# print(dowell_stratified_sampling_neyman(Yi, N, n, k, Ni, [1, 1, 1]))

