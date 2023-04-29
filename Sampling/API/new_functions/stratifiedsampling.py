import random
import time

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
    start_time = time.time()
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
    process_time = time.time() - start_time
    return sample, process_time
