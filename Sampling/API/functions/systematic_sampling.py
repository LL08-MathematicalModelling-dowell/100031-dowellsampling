from .sampleSize import dowellSampleSize
import random
from django.http import JsonResponse

def dowellSystematicSampling(systematicSamplingInput):
    
    df = systematicSamplingInput['sam']
    total_population = int(systematicSamplingInput['populations'])
    sample_sizes = int(systematicSamplingInput['sample_size'])
    
    error_margin = 0.05
    nn = dowellSampleSize(total_population, error_margin)
    print('NN is ', nn)
    K = round(total_population/sample_sizes)
    
    print('This is the sampling interval ', K)
    
    random_starting_point = random.randint(1, K)
    print('This is random starting point ', random_starting_point)
    
    
    systematic_sample = df.iloc[random_starting_point-1::K]
    
    return systematic_sample
    # Yi = systematicSamplingInput['population']
    
    # N = int(systematicSamplingInput['population_size'])
    # print('This is the population size ', N)
    # e = 0.05 # desired margin of error (5%)
    # n = dowellSampleSize(N, e)
    # # print('This is the sample size ',n)
    # # n = 9
    # # check if N divides n without remainder
    # if N % n == 0:
    #     print('N ', N)
    #     print('n ', n)
    #     k = N // n
    #     print('This is the k ', k)
    #     i = random.randint(0, k-1)
    #     print('This is i ', i)
    #     # select first unit randomly
    #     Yi = Yi[i:] + Yi[:i]
    #     print('This is the population ', Yi)
    #     sample_units = [Yi[ind] for ind in range(0, N, k)]
    #     print('Sample units ', sample_units)
    # else:
    #     print('False')
    #     k = N / n
    #     i = round(random.uniform(0, k))
    #     if i >= N:
    #         i -= 1
    #     # select first unit randomly
    #     Yi = Yi[i:] + Yi[:i]
    #     k = round(k)
    #     sample_units = [Yi[ind] for ind in range(0, N, k)]
    # return sample_units
    