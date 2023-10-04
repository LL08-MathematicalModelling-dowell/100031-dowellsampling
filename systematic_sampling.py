from .sampleSize import dowellSampleSize
import random

def dowellSystematicSampling(systematicSamplingInput):
    Yi = systematicSamplingInput['population']
    N = int(systematicSamplingInput['population_size'])
    e = 0.05 # desired margin of error (5%)
    n = dowellSampleSize(N, e)
    print(n)
    if N % n == 0:
        k = N // n
        i = random.randint(0, k-1)
        Yi = Yi[i:] + Yi[:i]
        sample_units = [Yi[ind] for ind in range(0, N, k)]
    else:
        k = N / n
        i = round(random.uniform(0, k))
        if i >= N:
            i -= 1
        Yi = Yi[i:] + Yi[:i]
        k = round(k)
        sample_units = [Yi[ind] for ind in range(0, N, k)]
    return sample_units