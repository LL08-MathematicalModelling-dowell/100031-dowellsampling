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


def dowellConnection(command, field, update_field):
    url = "http://uxlivinglab.pythonanywhere.com"
    payload = json.dumps(
        {
            "cluster": "dowellfunctions",
            "database": "dowellfunctions",
            "collection": "permutations",
            "document": "permutations",
            "team_member_ID": "1195001",
            "function_ID": "ABCDE",
            "command": command,
            "field": field,
            "update_field": update_field,
            "platform": "bangalore",
        }
    )

    headers = {"Content-Type": "application/json"}
    response = requests.request("POST", url, headers=headers, data=payload).json()
    data = json.loads(response)
    return data


def get_YI_data(inserted_id):
    data = dowellConnection("fetch", {"_id": inserted_id}, "")
    result_list = data.get('data', []) 
    cleaned_list = [{key: value for key, value in item.items() if key != '_id'} for item in result_list]
    return cleaned_list


def get_YI_data_new(inserted_id):
    url = "http://uxlivinglab.pythonanywhere.com"
    payload = json.dumps({
        "cluster": "dowellfunctions",
        "database": "dowellfunctions",
        "collection": "permutations",
        "document": "permutations",
        "team_member_ID": "1195001",
        "function_ID": "ABCDE",
        "command": 'fetch',
        "field": {"_id": f'{inserted_id}'},
        "update_field": '',
        "platform": "bangalore"
        })

    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data=payload).json()
    data = json.loads(response)
    result_list = data.get('data', []) 
    cleaned_list = [{key: value for key, value in item.items() if key != '_id'} for item in result_list]
    data_values = cleaned_list[0]['country']
    data_list = data_values.split(',')
    return data_list


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


@csrf_exempt
def insert_data(request):
    if request.method == "POST":
        try:
            data_str = request.body.decode("utf-8")
            if not data_str:
                raise ValueError("No data provided in the request body.")
            data = json.loads(data_str)
            response = dowellConnection("insert", data, "")
            return JsonResponse(response)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)


def all_sampling(raw_data):
    try:
        inserted_id = raw_data.get("insertedId")
        print(inserted_id)
        population_size = raw_data.get("populationSize")
        Yi_data_type = raw_data.get("result")
        sampling = raw_data.get("sampling")
        if Yi_data_type == "api":
            Yi = get_YI_data_new(inserted_id)
            print("running api")
            print(Yi,"yi")
        elif Yi_data_type == "link":
            excel_link = raw_data.get("link")
            if excel_link:
                print("running excel link")
                df = pd.read_csv(excel_link)
                print(df)
                list_of_lists = df.values.T.tolist()
                Yi = list_of_lists
            else:
                return {"error": "No link provided."}
        else:
            return {"error": "api or link not selected"}

        if sampling == "systematic_sampling":
            systematicSamplingInput = {
                "insertedId": inserted_id,
                "population": Yi,
                "population_size": population_size,
            }
            samples = dowellSystematicSampling(systematicSamplingInput)
            response = {"samples": samples}
            return response

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
            return response

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
            return response

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

            return response

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
                "Yi": Yi,
                "populationSize": population_size,
            }
            # print("stratified sampling input", stratifiedSamplingInput)
            samples = dowellStratifiedSampling(stratifiedSamplingInput)
            # id = get_event_id()
            response = {
                "samples": samples,
            }

            return response

        elif sampling == "quota_sampling":
            allocation_type = raw_data.get("allocationType")
            quotaSamplingInput = {
                "population_units": Yi,
                "population_size": population_size,
                "unit": allocation_type,
            }

            samples = dowellQuotaSampling(Yi, population_size, allocation_type)
            # id = get_event_id()
            response = {"samples": samples}
            return response

        elif sampling == "pps_sampling":
            size = raw_data.get("size")
            ppsSamplingInputs = {
                "population_units": Yi,
                "population_size": population_size,
                "size": size,
            }
            samples, process_time = dowellppsSampling(ppsSamplingInputs)
            print(samples)
            return {"samples": samples}
        elif sampling == "snowball_sampling":
            error = raw_data.get("error")
            reference = raw_data.get("reference")
            sample_size = dowellSampleSize(int(population_size), float(error))
            population_units = snowball_sampling_data()
            population_size = len(snowball_sampling_data())
            snowballSamplingInputs = {
                "population_size": population_size,
                "sample_size": sample_size,
                "population_units": snowball_sampling_data(),
                "reference": reference,
            }
            samples = dowellSnowballSampling(
                population_units, population_size, sample_size, reference
            )
            print(samples)
            return {"samples": samples}
        else:
            return {"message": f"{sampling} is not valid."}
    except Exception as e:
        return {"success": False, "message": str(e)}


@csrf_exempt
def samplingAPI(request, api_key):
    if request.method == "POST":
        data = json.loads(request.body)
        validate_api_count = processApikey(api_key, "DOWELL10011")
        data_count = json.loads(validate_api_count)
        if data_count["success"]:
            if data_count["total_credits"] >= 0:
                output = all_sampling(data)
                return JsonResponse(output, safe=False)
            else:
                return JsonResponse(
                    {
                        "success": False,
                        "message": data_count["message"],
                        "credits": data_count["total_credits"],
                    }
                )
        else:
            return JsonResponse({"success": False, "message": data_count["message"]})
    else:
        return HttpResponse("Method Not Allowed")


@csrf_exempt
def samplingInternalAPI(request):
    if request.method == "POST":
        data = json.loads(request.body)
        output = all_sampling(data)
        return JsonResponse(output, safe=False)
    else:
        return HttpResponse("Method Not Allowed")


# Request Data
{
    "number_of_stages": 2,
    "sampling_method": "Stratified Sampling",
    "body": {
        "stage_1": {
            "units_to_select": 10,
            "stratum_properties": [
                {
                    "stratum_name": "A",
                    "stratum_size": 100,
                    "stratum_units": [1, 2, 3, 4, 5],
                },
                {
                    "stratum_name": "B",
                    "stratum_size": 150,
                    "stratum_units": [6, 7, 8, 9, 10],
                },
            ],
        },
        "stage_2": {
            "units_to_select": 20,
            "sampling_method": "Random Sampling",
            "other_stage_2_property": "value",
        },
    },
}


@csrf_exempt
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


def dowell_twostage_sampling_view(request):
    if request.method == "POST":
        try:
            number_of_stages = request.POST.get("number_of_stages", None)
            sampling_method = request.POST.get("sampling_method", None)
            body = request.POST.get("body", None)

            sample_values, process_time, permutation_chosen = dowelltwostagesampling(
                number_of_stages, sampling_method, body
            )

            response_data = {
                "sample_values": sample_values,
                "process_time": process_time,
                "permutation_chosen": permutation_chosen,
            }

            return JsonResponse(response_data)
        except Exception as e:
            # Handle exceptions and return an error response if necessary
            return JsonResponse({"error": str(e)}, status=400)
    else:
        # Handle other HTTP methods if needed
        return JsonResponse({"error": "Only POST requests are supported."}, status=405)
