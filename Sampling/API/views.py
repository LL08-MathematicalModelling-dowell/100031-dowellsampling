from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse
import json
import requests
from rest_framework.decorators import api_view
from rest_framework.response import Response
from API.new_functions.stratifiedsampling import dowell_stratified_sampling_proportional
from API.new_functions.sample_size import dowell_sample_size

@csrf_exempt
# @api_view(['POST'])
def stratified_sampling(request):
    # Get input parameters from POST request
    api_url = 'http://localhost:8000/API/get_data/'
    response = requests.get(api_url)
    if response.status_code == 200:
        json_data = response.json()
        data = json_data['finalOutput']
 
    Yi = data
    N = 6
    k = 3
    Ni = [2, 2, 2]
    margin_of_error = 0.05
    confidence_level = 0.95

    # Calculate sample size using the dowell_sample_size() function
    n = dowell_sample_size(N, k, Ni, margin_of_error, confidence_level)
    # Call external API to get population units data
    # url = "http://100061.pythonanywhere.com/api/"
    # inserted_id = "63d8ed59790d8f03c13189aa"
    # payload = json.dumps({"inserted_id": inserted_id})
    # headers = {'Content-Type': 'application/json'}
    # response = requests.post(url, json =payload,headers=headers)
    # Yi = response['classifiedData']
    

    # Call dowellstratifiedsampling function
    output = dowell_stratified_sampling_proportional(Yi, N, n, k, Ni_list, ni_list)
    cities = output[0]
    process_time = output[1]
    
    response = {'cities': output, 'process_time': process_time}

    return JsonResponse(response)
def get_data(request):
    data = {
        "finalOutput": [
            ["India", "Germany"],
            ["Uttar Pradesh", "Georgia"],
            ["Pune", "Munich"],
            ["Mumbai", "Berlin"]
        ]
    }
    return JsonResponse(data)
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