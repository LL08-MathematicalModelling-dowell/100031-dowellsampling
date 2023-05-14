from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse
import json
import requests
from API.functions.stratifiedSampling import dowellStratifiedSampling
from API.functions.sampleSize import dowellSampleSize
from API.functions.systematic_sampling import dowellSystematicSampling
from API.functions.simpleRandomSampling import dowellSimpleRandomSampling
from API.functions.clusterSampling import dowellClusterSampling



@csrf_exempt
def get_data(request):
    data = {
        "finalOutput": [
            ["India", "Germany"],
            ["Uttar Pradesh", "Georgia"],
            ["Pune", "Munich"],
            ["Mumbai", "Berlin"],
            ["Delhi", "Hamburg"],
            ["Kolkata", "Hamburg"],
            ["MP", "Hamburg"],
        ]
    }
    return JsonResponse(data)

def get_YI_data():
    api_url = 'http://localhost:8000/API/get_data/'
    response = requests.get(api_url)
    if response.status_code == 200:
        json_data = response.json()
        data = json_data['finalOutput']
    return data

def stratified_sampling(request):
    # Get input parameters from POST request
    if request.method == 'POST':
        allocation_type = request.POST.get('allocationType')
        sampling_type = request.POST.get('samplingType')
        inserted_id = request.POST.get('insertedId')
        replacement = request.POST.get('replacement') == 'true'
        populationSize = request.POST.get('populationSize')


        # Retrieve Yi data (you need to implement this)
        Yi = get_YI_data()

        stratifiedSamplingInput = {
            'e': 0.1,
            'allocationType': allocation_type,
            'samplingType': sampling_type,
            'insertedId': inserted_id,
            'replacement': replacement,
            'Yi': Yi,
            'populationSize': populationSize
        }

        # Call the stratified_sampling API function
        result = dowellStratifiedSampling(stratifiedSamplingInput)
    else:
        result = {
            'error': 'Invalid request method'
        }
    return JsonResponse(result)

def systematic_sampling(request):
    # Retrieve user input for Yi and population_size
    if request.method == 'POST':
        Yi = get_YI_data()
        population_size = request.POST.get('population_size')
        systematicSamplingInput = {
            'population': Yi,
            'population_size': population_size
        }
        # Convert population_size to an integer
        population_size = int(population_size)

        # Perform systematic sampling using Yi and population_size
        samples = dowellSystematicSampling(systematicSamplingInput)

        # Prepare the response
        response = {
            'samples': samples
        }
    else:
        response = {
            'error': 'Invalid request method'
        }
    return JsonResponse(response)


def simple_random_sampling(request):
    if request.method == 'POST':
        Yi = get_YI_data()
        e = request.POST.get('e')
        N = request.POST.get('N')
        n = dowellSampleSize(int(N),float(e))
        method = request.POST.get('method')
        simpleRandomSamplingInput = {
            'Yi': Yi,
            'N': int(N),
            'n': n,
            'method': method
        }
        samples = dowellSimpleRandomSampling(simpleRandomSamplingInput)
        response = {
            'samples': samples
        }
    response = samples
    return JsonResponse(response)


def sampling_input(request):
    return render(request, 'sampling_inputs.html')

def sampling_input(request):
    return render(request, 'sampling_inputs.html')

def cluster_sampling(request):
    if request.method == 'POST':
        Yi = get_YI_data()
        e = request.POST.get('e')
        N = request.POST.get('N')
        M = request.POST.get('M')
        hi = request.POST.get('hi')

        clusterSamplingInput = {
            'Yi': Yi,
            'e': float(e),
            'N': int(N),
            'M': int(M),            
            'hi': int(hi)
        }

        samples = dowellClusterSampling(clusterSamplingInput)
        response = {
            'samples': samples
        }
    response = samples
    return JsonResponse(response, safe=False)

'''
Types of sampling
1. Stratified Random Sampling
Request
{

}

Response
{

}

2. Systematic Sampling
Request
{

}

Response
{

}

3. Purposive Sampling
Request
{

}

Response
{

}

4. Cluster
Request
{

}

Response
{

}

'''
