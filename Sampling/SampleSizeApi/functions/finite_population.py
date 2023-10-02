from .z_score import get_z_score
import math
import time

def calculate_sample_size_with_known_sd(population_size, error, confidence_level, standard_deviation):
    process_time = 0
    z = get_z_score(confidence_level)
    p = standard_deviation
    q = 1 - p
    numerator = (z ** 2) * p * q
    denominator = (error ** 2) * (1 + (((z ** 2) * p * q) / (error ** 2 * population_size)))
    sample_size = numerator / denominator
    process_time = time.process_time()
    method_used = 'finite_population'
    return math.ceil(sample_size), process_time, method_used