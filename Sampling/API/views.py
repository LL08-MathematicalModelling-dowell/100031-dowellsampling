import json
import requests
import pandas as pd
import time

from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse

from API.functions.stratifiedSampling import dowellStratifiedSampling
from API.functions.sampleSize import dowellSampleSize
from API.functions.systematic_sampling import dowellSystematicSampling
from API.functions.simpleRandomSampling import dowellSimpleRandomSampling
from API.functions.clusterSampling import dowellClusterSampling
from API.functions.purposiveSampling import dowellPurposiveSampling
from API.functions.quotaSampling import dowellQuotaSampling
from API.functions.ppsSampling import dowellppsSampling
from API.functions.get_event_id import get_event_id
from API.functions.API_Key_System import processApikey
from API.functions.snowballSampling import dowellSnowballSampling


from API.functions.snowballSampling import dowellSnowballSampling

def get_YI_data():
    header = {"content-type": "application/json"}
    data = json.dumps({"insertedId": "646d188771d319c4cf8e182a"})
    url = "http://100061.pythonanywhere.com/function/"
    response = requests.request("POST", url, data=data, headers=header).json()
    data = response["finalOutput"]
    return data

def get_YI_data_new():
    hardcoded_data = [
        "Apple",
        "Banana",
        "Cherry",
        "Date",
        "Fig",
        "Grape",
        "Kiwi",
        "Lemon",
        "Mango",
        "Orange",
        "Peach",
        "Pear",
        "Quince",
        "Raspberry",
        "Strawberry",
        "Watermelon",
        "Blueberry",
        "Pineapple",
        "Pomegranate",
        "Guava",
        "Jackfruit",
        "Apricot",
        "Avocado",
        "Blackberry",
        "Blackcurrant",
        "Coconut",
        "Custard apple",
        "Dragonfruit",
        "Durian",
        "Elderberry",
        "Feijoa",
        "Gooseberry",
        "Grapefruit",
        "Honeyberry",
        "Huckleberry",
    ]
    return hardcoded_data


def snowball_sampling_data():
    data = [
    {"name": "John Doe", "connections": ["Jane Doe", "Peter Smith"]},
    {"name": "Jane Doe", "connections": ["John Doe", "Susan Jones"]},
    {"name": "Peter Smith", "connections": ["John Doe", "Mary Johnson"]},
    {"name": "Susan Jones", "connections": ["Jane Doe", "David Williams"]},
    {"name": "Mary Johnson", "connections": ["Peter Smith", "David Williams"]},
    {"name": "David Williams", "connections": ["Mary Johnson", "Susan Jones"]},
]
    return data

def all_sampling(raw_data):
    try:
        inserted_id = raw_data.get("insertedId")
        population_size = raw_data.get("populationSize")
        Yi_data_type = raw_data.get("result")
        sampling = raw_data.get("sampling")
        if Yi_data_type == "api":
            Yi = get_YI_data_new()
        elif Yi_data_type == "upload":
            excel_link = raw_data.get("link")
            if excel_link:
                df = pd.read_excel(excel_link)
                list_of_lists = df.values.T.tolist()
                Yi = list_of_lists
            else:
                return ({"error": "No link provided."})
        else:
            return ({"error": "api or link not selected"})

        if sampling == "systematic_sampling":
            systematicSamplingInput = {
                "insertedId": inserted_id,
                "population": Yi,
                "population_size": population_size,
            }
            samples = dowellSystematicSampling(systematicSamplingInput)
            response = {"samples": samples}
            return (response)

        elif sampling == "simple_random_sampling":
            error = raw_data.get("error")
            method = raw_data.get("sampling_method")
            n = dowellSampleSize(int(population_size), float(error))
            simpleRandomSamplingInput = {
                "insertedId": inserted_id,
                "Yi": Yi,
                "N": int(population_size),
                "e": float(error),
                "method": method,
                "n": n,
            }
            samples = dowellSimpleRandomSampling(simpleRandomSamplingInput)
            response = {"samples": samples["sampleUnits"]}
            return (response)

        elif sampling == "purposive_sampling":
            print("purposive sampling running ")
            error = raw_data.get("error")
            unit = raw_data.get("unit")
            # print("yi", Yi)
            # new_yi = sum(Yi, [])
            # print("new yi",new_yi)
            # print("unit", unit)
            purposiveSamplingInput = {
                "insertedId": inserted_id,
                "Yi": Yi,
                "unit": unit,
                "error": float(error),
                "populationSize": int(population_size),
            }

            samples = dowellPurposiveSampling(purposiveSamplingInput)
            # id = get_event_id()
            response = {
                "samples": samples,
            }
            return (response)

        elif sampling == "cluster_sampling":
            error = raw_data.get("error")
            numberOfClusters = raw_data.get("numberOfClusters")
            sizeOfCluster = raw_data.get("sizeOfCluster")
            clusterSamplingInput = {
                "Yi": Yi,
                "e": float(error),
                "N": int(population_size),
                "M": int(numberOfClusters),
                "hi": int(sizeOfCluster),
            }

            samples = dowellClusterSampling(clusterSamplingInput)
            # id = get_event_id() 
            response = {
                "samples": samples,
            }

            return (response)

        elif sampling == "stratified_sampling":
            allocation_type = raw_data.get("allocationType")
            sampling_type = raw_data.get("samplingType")
            replacement = raw_data.get("replacement")
            error = raw_data.get("error")
            stratifiedSamplingInput = {
                "insertedId": inserted_id,
                "e": error,
                "allocationType": allocation_type,
                "samplingType": sampling_type,
                "replacement": replacement,
                "Yi": get_YI_data(),
                "populationSize": population_size,
            }
            # print("stratified sampling input", stratifiedSamplingInput)
            samples = dowellStratifiedSampling(stratifiedSamplingInput)
            # id = get_event_id() 
            response = {
                "samples": samples,
            }

            return (response)

        elif sampling == "quota_sampling":
            allocation_type = raw_data.get("allocationType")
            quotaSamplingInput = {
                "population_units": Yi,
                "population_size": population_size,
                "unit": allocation_type,
            }

            samples, process_time = dowellQuotaSampling(**quotaSamplingInput)
            # id = get_event_id()
            response = {"samples": samples}
            return (response)

        elif sampling == "pps_sampling":
            size = raw_data.get("size")
            ppsSamplingInputs = {
            "population_units": Yi,
            "population_size": population_size,
            "size": size,
        }
            samples, process_time = dowellppsSampling(ppsSamplingInputs)
            print(samples)
            return ({"samples": samples})
        elif sampling == "snowball_sampling":
            error = raw_data.get("error")
            reference = raw_data.get("reference")
            sample_size = dowellSampleSize(int(population_size), float(error))
            snowballSamplingInputs = {
            "population_size": population_size,
            "sample_size" : sample_size,
            "population_units" : snowball_sampling_data(),
            "reference" : reference
        }
            samples= dowellSnowballSampling(**snowballSamplingInputs)
            print(samples)
            return ({"samples": samples})
        else:
            return ({
                "message":f"{sampling} is not valid."
            })
    except Exception as e:
        return ({
            "success":False,
            "message": str(e)
        })
    
@csrf_exempt
def samplingAPI(request, api_key):
    if (request.method=="POST"):
        data=json.loads(request.body)
        validate_api_count = processApikey(api_key, "DOWELL10011")
        data_count = json.loads(validate_api_count)
        if data_count['success'] :
            if data_count['total_credits'] >= 0:
                output = all_sampling(data)
                return JsonResponse(output, safe = False)
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

@csrf_exempt
def samplingInternalAPI(request):
    if (request.method=="POST"):
        data=json.loads(request.body)
        output = all_sampling(data)
        return JsonResponse(output, safe = False)
    else:
        return HttpResponse("Method Not Allowed")


def dowelltwostagesampling(number_of_stages, sampling_method, body):
    # Define the number of stages
    S = number_of_stages if number_of_stages != None else 0
    # S = int(input("Enter the number of stages: "))

    if number_of_stages not in [1, 2]:
        raise ValueError("Number of stages must be 1 or 2.")

    # List to store the selected units at each stage
    sample_values = []

    # Iterate over each stage
    i = 0
    while i < S:
        print(sampling_method[i])

        print(f"\nStage {i}:")

        # Choose the sampling method for the current stage
        # sampling_method = dowellindex()

        # Determine the number of units to be selected in the current stage

        # Check if the user entered "0" for the current stage
        if sampling_method[i] == 0:
            print("Sampling stopped.")
            break
        # Check if the selected sampling method is Simple Random Sampling
        elif sampling_method[i] == 1 or sampling_method[i] == 2:
            sample = dowellSimpleRandomSampling(body)
        # Check if the selected sampling method is Stratified Sampling
        elif sampling_method[i] == 3 or sampling_method[i] == 4:
            sample = dowellStratifiedSampling(body)
        # Check if the selected sampling method is Systematic Sampling
        elif sampling_method[i] == 5 or sampling_method[i] == 6:
            sample = dowellSystematicSampling(body)
        # Check if the selected sampling method is Cluster Sampling
        elif sampling_method[i] == 7:
            sample = dowellClusterSampling(body)
        # Check if the selected sampling method is Purposive Sampling
        elif sampling_method[i] == 8:
            sample = dowellPurposiveSampling(body)
        # Check if the selected sampling method is PPS Sampling
        elif sampling_method[i] == 9 or sampling_method[i] == 10:
            print(body)
            sample = dowellppsSampling(body)
        # Check if the selected sampling method is Snowball Sampling
        elif sampling_method[i] == 11:
            sample = dowellSnowballSampling(body)
        # Check if the selected sampling method is Quota Sampling
        elif sampling_method[i] == 12:
            sample = dowellQuotaSampling(body)
        else:
            print("Invalid sampling method.")
            continue
        i += 1
        # Add the selected sample to the list of sample values
        sample_values.append(sample)


    # Process time
    process_time = time.process_time()

    # Permutation chosen
    permutation_chosen = None  # Placeholder for permutation chosen

    return sample_values, process_time, permutation_chosen


