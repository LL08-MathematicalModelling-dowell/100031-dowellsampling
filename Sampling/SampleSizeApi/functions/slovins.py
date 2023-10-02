import math
import time
def calculate_sample_size_using_slovin(population_size, error):
    process_time = 0
    sample_size = population_size / (1 + population_size * error ** 2)
    sample_size_rounded = math.ceil(sample_size)
    process_time = time.process_time()
    method_used = 'slovin'
    if 1 < sample_size_rounded < 500:
        return sample_size_rounded , process_time, method_used
    else:
        return "Sample size is not adequate", process_time, method_used