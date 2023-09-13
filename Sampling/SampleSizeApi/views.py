import json
import math
import time
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from API.functions.API_Key_System import processApikey
import random

def calculate_sample_size(data):
    try:
        population_size = data.get('population_size')
        error = float(data.get('error', 0))
        confidence_level = float(data.get('confidence_level', 0.95))
        standard_deviation = data.get('standard_deviation')

        if population_size is not None:
            population_size = int(population_size)
            if population_size <= 0 or error <= 0:
                return JsonResponse({'error': 'Invalid input. Population size and error must be positive.'}, status=400)
            standard_deviation = calculate_standard_deviation(error, population_size, confidence_level)
            if standard_deviation is not None:
                standard_deviation = float(standard_deviation)
                sample_size, process_time, method_used = calculate_sample_size_with_known_sd(population_size, error, confidence_level, standard_deviation)
            else:
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

def calculate_sample_size_without_pop_size(error, confidence_level, standard_deviation):
    process_time = 0
    z = get_z_score(confidence_level)
    p = standard_deviation
    sample_size = (z ** 2 * p * (1 - p)) / (error ** 2)
    process_time = time.process_time()
    method_used = 'infinite_population'
    return math.ceil(sample_size) , process_time, method_used

def get_z_score(confidence_level):
    if confidence_level == 0.90:
        return 1.645
    elif confidence_level == 0.95:
        return 1.96
    elif confidence_level == 0.99:
        return 2.58
    else:
        raise ValueError("Invalid confidence level. Supported values: 0.90, 0.95, 0.99")
    
    
def calculate_standard_deviation(error, population_size, confidence_level):
    try:
        z = get_z_score(confidence_level)
        numerator = (z ** 2 * population_size * (1 - error)) / (error ** 2)
        return math.sqrt(numerator / population_size)
    except (ValueError, ZeroDivisionError):
        return None 



@csrf_exempt
def sample_size(request):
    if (request.method=="POST"):
        data=json.loads(request.body)
        return calculate_sample_size(data)
    else:
        return HttpResponse("Method Not Allowed")

@csrf_exempt
def sample_size_api(request, api_key):
    if (request.method=="POST"):
        data=json.loads(request.body)
        validate_api_count = processApikey(api_key, "DOWELL10032")
        data_count = json.loads(validate_api_count)
        if data_count['success'] :
            if data_count['total_credits'] >= 0:
                return calculate_sample_size(data)
            else:
                return JsonResponse({
                    "success": False,
                    "message": data_count['message'],
                    "credits": data_count['total_credits']
                })
        else:
            return JsonResponse({
                "success": False,
                "message": data_count['message']
            })
    else:
        return HttpResponse("Method Not Allowed")
