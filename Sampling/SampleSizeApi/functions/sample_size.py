from .finite_population import *
from .infinite_population import *
from .slovins import *
from .sd_calaculate import *
from .z_score import *
from django.http import JsonResponse, HttpResponse
import random

def calculate_sample_size(data):
    try:
        population_size = data.get('population_size')
        error = float(data.get('error', 0))
        confidence_level = float(data.get('confidence_level', 0.95))
        standard_deviation = data.get('standard_deviation')
        
        if standard_deviation is not None:
            if standard_deviation <=.01 or standard_deviation >=.99:
                return JsonResponse({'error': 'Invalid input. Standard deviation must be between 0.01 and 0.99.'}, status=400)
        else:
            pass

        if population_size is not None:
            population_size = int(population_size)
            if population_size <= 0 or error <= 0:
                return JsonResponse({'error': 'Invalid input. Population size and error must be positive.'}, status=400)
            if standard_deviation is not None:
                standard_deviation = float(standard_deviation)
                sample_size, process_time, method_used = calculate_sample_size_with_known_sd(population_size, error, confidence_level, standard_deviation)
            else:
                # standard_deviation = calculate_standard_deviation(error, population_size, confidence_level)
                sample_size, process_time, method_used = calculate_sample_size_using_slovin(population_size, error)
        else:
            if standard_deviation is not None:
                standard_deviation = float(standard_deviation)
                sample_size, process_time, method_used = calculate_sample_size_without_pop_size(error, confidence_level, standard_deviation)
            else:
                population_size = random.randint(100000,1000000)
                print(population_size)
                sample_size, process_time, method_used = calculate_sample_size_using_slovin(population_size, error)

        return JsonResponse({'sample_size': sample_size, 'process_time': process_time, 'method_used': method_used, 'success':True})

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)