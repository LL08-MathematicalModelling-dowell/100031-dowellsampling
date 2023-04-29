from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse
import json

import requests
from API.functions.stratifiedSampling import dowellStratifiedSampling
from rest_framework.decorators import api_view
from rest_framework.response import Response
from API.new_functions.stratifiedsampling import dowellstratifiedsampling

@csrf_exempt
# @api_view(['POST'])
def stratified_sampling(request):
    # Get input parameters from POST request
    api_url = 'http://localhost:8000/API/get_data/'
    response = requests.get(api_url)
    if response.status_code == 200:
        json_data = response.json()
        data = json_data['finalOutput']
    city_to_num = {}
    num_to_city = {}
    flat_data = []
    for city_list in data:
        for city in city_list:
            if city not in city_to_num:
                num = len(city_to_num)
                city_to_num[city] = num
                num_to_city[num] = city
            flat_data.append(city_to_num[city])
    Yi = flat_data
    N = 60
    n = 7
    k = 5
    Ni_list = [9,5,20,19,3,4,5,6,7,]
    ni_list = [2, 1, 1, 4,1,9]
    # Call external API to get population units data
    # url = "http://100061.pythonanywhere.com/api/"
    # inserted_id = "63d8ed59790d8f03c13189aa"
    # payload = json.dumps({"inserted_id": inserted_id})
    # headers = {'Content-Type': 'application/json'}
    # response = requests.post(url, json =payload,headers=headers)
    # Yi = response['classifiedData']
    

    # Call dowellstratifiedsampling function
    output = dowellstratifiedsampling(Yi, N, n, k, Ni_list, ni_list)
    cities = output[0]
    process_time = output[1]
    final_output = [num_to_city[num] for num in cities]
    
    response = {'cities': final_output, 'process_time': process_time}

    return JsonResponse(response)
def get_data(request):
    data = {
        "finalOutput": [
            ["India", "Germany"],
            ["Uttar Pradesh", "Georgia"],
            ["Pune", "Munich"],
            ["Mumbai", "Berlin"],
            ["Delhi", "Hamburg"],
            ["Bangalore", "Frankfurt"],
            ["Chennai", "Stuttgart"],
            ["Kolkata", "Dresden"],
            ["Hyderabad", "Cologne"],
            ["Ahmedabad", "Leipzig"],
            ["Jaipur", "Dortmund"],
            ["Surat", "Essen"],
            ["Lucknow", "Düsseldorf"],
            ["Kanpur", "Bremen"],
            ["Nagpur", "Hanover"],
            ["Patna", "Duisburg"],
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