from .z_score import get_z_score
import math
import time

def calculate_sample_size_without_pop_size(error, confidence_level, standard_deviation):
    process_time = 0
    z = get_z_score(confidence_level)
    p = standard_deviation
    sample_size = (z ** 2 * p * (1 - p)) / (error ** 2)
    process_time = time.process_time()
    method_used = 'infinite_population'
    return math.ceil(sample_size) , process_time, method_used