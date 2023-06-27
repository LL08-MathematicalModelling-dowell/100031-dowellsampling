import pandas as pd
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
from API.functions.purposiveSampling import dowellPurposiveSampling
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .functions.searchFunction import dowell_purposive_sampling
import json
import requests
import pprint

def get_event_id():

    url="https://uxlivinglab.pythonanywhere.com/create_event"

    data={
        "platformcode":"FB" ,
        "citycode":"101",
        "daycode":"0",
        "dbcode":"pfm" ,
        "ip_address":"192.168.0.41", # get from dowell track my ip function 
        "login_id":"lav", #get from login function
        "session_id":"new", #get from login function
        "processcode":"1",
        "location":"22446576", # get from dowell track my ip function 
        "objectcode":"1",
        "instancecode":"100051",
        "context":"afdafa ",
        "document_id":"3004",
        "rules":"some rules",
        "status":"work",
        "data_type": "learn",
        "purpose_of_usage": "add",
        "colour":"color value",
        "hashtags":"hash tag alue",
        "mentions":"mentions value",
        "emojis":"emojis",
        "bookmarks": "a book marks"
    }

    r=requests.post(url,json=data)
    if r.status_code == 201:
        return json.loads(r.text)
    else: 
        return json.loads(r.text)['error']

@csrf_exempt
def get_data(request):
    header = { 'content-type': 'application/json'}
    data = json.dumps({
   "insertedId":"646d188771d319c4cf8e182a"
})
    url = 'http://100061.pythonanywhere.com/function/'
    response = requests.request("POSR",url, data=data, headers=header).json()
    return JsonResponse(response)

@csrf_exempt
def get_YI_data():
    header = { 'content-type': 'application/json'}
    data = json.dumps({
   "insertedId":"646d188771d319c4cf8e182a"
})
    url = 'http://100061.pythonanywhere.com/function/'
    response = requests.request("POST",url, data=data, headers=header).json()
    data = response['finalOutput']
    return data

def systematic_sampling(request):
    if request.method == 'POST':
        data = request.POST.get('data')
        inserted_id = request.POST.get('insertedId')
        population_size = request.POST.get('populationSize')
        result = request.POST.get('result')
        if data == 'api':
            Yi = get_YI_data()
        elif data == 'upload':
            uploaded_file = request.FILES.get('file')
            if uploaded_file:
                df = pd.read_excel(uploaded_file)
                list_of_lists = df.values.T.tolist()
                Yi = list_of_lists
            else:
                return JsonResponse({'error': 'No file uploaded.'})
        
        systematicSamplingInput = {
            'insertedId': inserted_id,
            'population': Yi,
            'population_size': population_size
        }

        samples = dowellSystematicSampling(systematicSamplingInput)
        response = {
            'samples': samples
        }
        if result == 'Table':
            return render(request, 'result.html', {'response': response})
        return JsonResponse(response, safe=False)

def simple_random_sampling(request):
    if request.method == 'POST':
        data = request.POST.get('data')
        inserted_id = request.POST.get('insertedId')
        N = request.POST.get('populationSize')
        e = request.POST.get('e')
        method = request.POST.get('samplingType')
        n = dowellSampleSize(int(N),float(e))
        result = request.POST.get('result')
        if data == 'api':
            Yi = get_YI_data()
        elif data == 'upload':
            uploaded_file = request.FILES.get('file')
            if uploaded_file:
                df = pd.read_excel(uploaded_file)
                list_of_lists = df.values.T.tolist()
                Yi = list_of_lists
            else:
                return JsonResponse({'error': 'No file uploaded.'})
        
        simpleRandomSamplingInput = {
            'insertedId': inserted_id,
            'Yi': Yi,
            'N': int(N),
            'e': float(e),
            'method': method,
            'n': n
        }

        samples = dowellSimpleRandomSampling(simpleRandomSamplingInput)
        response = {"samples": samples['sampleUnits']}
        if result == 'Table':
            return render(request, 'result.html', {'response': response})
        return JsonResponse(response, safe=False)

def purposive_sampling(request):
    if request.method == 'POST':
        data = request.POST.get('data')
        inserted_id = request.POST.get('insertedId')
        unit = request.POST.get('unit')
        e = request.POST.get('e')
        N = request.POST.get('N')
        result = request.POST.get('result')
        if data == 'api':
            Yi = get_YI_data()
        elif data == 'upload':
            uploaded_file = request.FILES.get('file')
            if uploaded_file:
                df = pd.read_excel(uploaded_file)
                list_of_lists = df.values.T.tolist()
                Yi = list_of_lists
            else:
                return JsonResponse({'error': 'No file uploaded.'})
        new_yi = sum(Yi, [])
        purposiveSamplingInput = {
            'insertedId': inserted_id,
            'Yi': new_yi,
            'unit': unit,
            'e': float(e),
            'N': int(N),
        }

        samples = dowellPurposiveSampling(purposiveSamplingInput)
        response = {
            'samples': samples
        }
        if result == 'Table':
            return render(request, 'result.html', {'response': response})
        return JsonResponse(response, safe=False)


def cluster_sampling(request):
    if request.method == 'POST':
        data = request.POST.get('data')
        M = request.POST.get('numberOfClusters')
        inserted_id = request.POST.get('insertedId')
        N = request.POST.get('populationSize')
        e = request.POST.get('e')
        hi = request.POST.get('sizeOfCluster')
        result = request.POST.get('result')
        # Retrieve Yi data (you need to implement this)
        if data == 'api':
            Yi = get_YI_data()
        elif data == 'upload':
            uploaded_file = request.FILES.get('file')
            if uploaded_file:
                df = pd.read_excel(uploaded_file)
                list_of_lists = df.values.T.tolist()
                Yi = list_of_lists
            else:
                return JsonResponse({'error': 'No file uploaded.'})
        
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
        
        if result == 'Table':
            return render(request, 'result.html', {'response': response})
        return JsonResponse(response, safe=False)

def stratified_sampling(request):
    if request.method == 'POST':
        data = request.POST.get('data')
        inserted_id = request.POST.get('insertedId')
        allocation_type = request.POST.get('allocationType')
        sampling_type = request.POST.get('samplingType')
        replacement = request.POST.get('replacement') == 'true'
        populationSize = request.POST.get('populationSize')
        result = request.POST.get('result')
        if data == 'api':
            Yi = get_YI_data()
        elif data == 'upload':
            uploaded_file = request.FILES.get('file')
            if uploaded_file:
                df = pd.read_excel(uploaded_file)
                list_of_lists = df.values.T.tolist()
                Yi = list_of_lists
            else:
                return JsonResponse({'error': 'No file uploaded.'})
        
        stratifiedSamplingInput = {
            'insertedId': inserted_id,
            'e': 0.1,
            'allocationType': allocation_type,
            'samplingType': sampling_type,
            'replacement': replacement,
            'Yi': Yi,
            'populationSize': populationSize
        }

        samples = dowellStratifiedSampling(stratifiedSamplingInput)
        id = get_event_id()
        response = {
            'samples': samples
        }
        response = {"event_id":id['event_id'],"samples": samples['sampleUnits']}
        
        if result == 'Table':
            return render(request, 'result.html', {'response': response})
        return JsonResponse(response, safe=False)



@api_view(['GET'])
def dowell_search(request):
    search_count = int(request.GET.get('search_count', 0))
    user_field_str = request.GET.get('user_field','{}')
    search_criteria = []
    user_field = json.loads(user_field_str)
    for i in range(search_count):
        key = request.GET.get(f'key{i}', '')
        value = request.GET.get(f'value{i}', '')
        search_criteria.append((key, value))
    print(user_field)
    sample_values = dowell_purposive_sampling(search_criteria,user_field)
    return Response(sample_values)

def search(request):
    return render(request, 'search_function.html')



def sampling_input(request):
    return render(request, 'sampling_inputs.html')

def stratified_sampling_input(request):
    return render(request, 'stratified_sampling_input.html')

def systematic_sampling_input(request):
    return render(request, 'systematic_sampling_input.html')

def simple_random_sampling_input(request):
    return render(request, 'simple_random_sampling_input.html')

def cluster_sampling_input(request):
    return render(request, 'cluster_sampling_input.html')

def purposive_sampling_input(request):
    return render(request, 'purposive_sampling_input.html')




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