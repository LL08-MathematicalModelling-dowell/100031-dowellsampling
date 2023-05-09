import random
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse
import json
import requests
from rest_framework.decorators import api_view
from rest_framework.response import Response
from API.new_functions.stratifiedsampling import dowell_stratified_sampling_proportional
from API.new_functions.sample_size import dowellSampleSize
from API.new_functions.systematicSampling import dowellSystematicSampling

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


# @api_view(['POST'])
def stratified_sampling(request):
    # Get input parameters from POST request
    Yi = get_YI_data()
    N = 6
    k = 3
    Ni = [2, 2, 2]
    margin_of_error = 0.05
    n= dowellSampleSize(N, margin_of_error)
    ni =[1,1,1]
    # Call dowellstratifiedsampling function
    output = dowell_stratified_sampling_proportional(Yi, N, n, k, Ni, ni)
    cities = output[0]
    process_time = output[1]
    response = {'cities': cities, 'process_time': process_time}
    return JsonResponse(response)


def systematic_sampling(request):
    Yi = get_YI_data()
    N = len(Yi)
    e = 0.05 # desired margin of error (5%)
    n = dowellSampleSize(N, e)
    samples = dowellSystematicSampling(Yi, n)
    response = {
            'samples': samples
        }
    return JsonResponse(response)





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