import math


def dowellSampleSize(N, e ):
    try:
        population_size = N
        error = e
        sample_size= calculate_sample_size_using_slovin(population_size, error)
        return sample_size

    except Exception as e:
        return e


def calculate_sample_size_using_slovin(population_size, error):
    sample_size = population_size / (1 + population_size * error ** 2)
    sample_size_rounded = math.ceil(sample_size)
    if 1 < sample_size_rounded < 500:
        return sample_size_rounded 
    else:
        return "Sample size is not adequate"


