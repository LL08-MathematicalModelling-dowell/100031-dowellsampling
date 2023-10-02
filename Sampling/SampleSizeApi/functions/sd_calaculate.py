from .z_score import get_z_score
import math
def calculate_standard_deviation(population_size, error, confidence_level):
    try:
        z = get_z_score(confidence_level)
        if error <= 0 or error >= 1:
            raise ValueError("Error should be a positive value between 0 and 1")
        sample_size = (z ** 2 * 0.25) / (error ** 2)
        standard_deviation = math.sqrt(0.25 * (1 - 0.25) / sample_size)
        
        return standard_deviation
    except (ValueError, ZeroDivisionError):
        return None