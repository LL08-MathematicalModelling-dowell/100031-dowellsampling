import json
import requests
import pandas as pd
import time

from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse

from .functions.stratifiedSampling import dowellStratifiedSampling
from .functions.sampleSize import dowellSampleSize
from .functions.systematic_sampling import dowellSystematicSampling
from .functions.simpleRandomSampling import dowellSimpleRandomSampling
from .functions.clusterSampling import dowellClusterSampling
from .functions.purposiveSampling import dowellPurposiveSampling
from .functions.quotaSampling import dowellQuotaSampling
from .functions.ppsSampling import dowellppsSampling
from .functions.get_event_id import get_event_id
from .functions.API_Key_System import processApikey
from .functions.snowballSampling import dowellSnowballSampling


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
        population_size = raw_data.get("populationSize")
        Yi_data_type = raw_data.get("result")
        strata_variable = raw_data.get("strata_variable")
        sampling = raw_data.get("sampling")
        cluster = raw_data.get('cluster')
        if Yi_data_type == "api":
            Yi = get_YI_data_new(inserted_id)
        elif Yi_data_type == "link":
            excel_link = raw_data.get("link")
            if excel_link:
                
                sample_size = raw_data.get("sample_size")
                df = pd.read_csv(excel_link)
                list_of_lists = df.values.T.tolist()
                Yi = list_of_lists
                
                population_sizes = df.shape[0]
                
            else:
                return {"error": "No link provided."}
        else:
            return {"error": "api or link not selected"}

        if sampling == "systematic_sampling":
            systematicSamplingInput = {
                "insertedId": inserted_id,
                # "population": Yi,
                # "population_size": population_size,
                # new undates
                'populations': population_sizes,
                'sample_size': sample_size,
                "sam": df,
            }
            samples = dowellSystematicSampling(systematicSamplingInput)
            sample = samples.values.T.tolist()
            # dic = samples.to_dict('series')
            # response = {"samples": samples}
            
            # systematic_sample_json = response.to_json(orient='records')
            # systematic_sample_json = json.dumps(response)
            # systematic_sample_json = response.to_json(orient='records')
            # systematic_sample_json = json.dumps(response)

            # Return the data as a JSON response
            # return JsonResponse(systematic_sample_json, safe=False)
            # return response
            # systematic_sample_json = response.to_json(orient='records')

            # # Return the JSON string as a JsonResponse
            # return JsonResponse(json.loads(systematic_sample_json), safe=False)
            # systematic_sample_dict = response.to_dict(orient='records')
            response = {"samples": sample}
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
                # new undates
                'populations': population_sizes,
                'sample_size': sample_size,
                "sam": df,
            }
            samples = dowellSimpleRandomSampling(simpleRandomSamplingInput)
            response = {"samples": samples["sampleUnits"]}
            return response

        elif sampling == "purposive_sampling":
            error = raw_data.get("error")
            unit = raw_data.get("unit")
            
            purposiveSamplingInput = {
                "insertedId": inserted_id,
                "Yi": Yi,
                "unit": unit,
                "error": float(error),
                "populationSize": int(population_sizes),
                # ============
                'populations': population_sizes,
                'sample_size': sample_size,
                "sam": df,
                
            }

            samples = dowellPurposiveSampling(purposiveSamplingInput)
            # id = get_event_id()
            
            sample = samples.values.T.tolist()
            response = {"samples": sample}
            return response

        elif sampling == "cluster_sampling":
            error = raw_data.get("error")
            numberOfClusters = raw_data.get("numberOfClusters")
            sizeOfCluster = raw_data.get("sizeOfCluster")
            clusterSamplingInput = {
                "Yi": Yi,
                "e": float(error),
                "N": int(population_sizes),
                "M": int(numberOfClusters),
                "hi": int(sizeOfCluster),
                # ==============
                'populations': population_sizes,
                'sample_size': sample_size,
                "sam": df,
                "cluster": cluster,
            }

            sample = dowellClusterSampling(clusterSamplingInput)
            # id = get_event_id()
            # response = {
            #     "samples": samples,
            # }
            samples = sample.values.T.tolist()            
            response = {"samples": samples}
            return response

        elif sampling == "stratified_sampling":
            print("Running....")
            allocation_type = raw_data.get("allocationType")
            sampling_type = raw_data.get("samplingType")
            replacement = raw_data.get("replacement")
            error = raw_data.get("error")
            print('This is errors ', error)
            stratifiedSamplingInput = {
                "insertedId": inserted_id,
                "e": error,
                "allocationType": allocation_type,
                "samplingType": sampling_type,
                "replacement": replacement,
                "Yi": Yi,
               
                # ==============
                'populations': population_sizes,
                'sample_size': sample_size,
                "sam": df,
                "strata_variable": strata_variable,
            }
            print('Here is where i am', dowellStratifiedSampling(stratifiedSamplingInput))
            sample = dowellStratifiedSampling(stratifiedSamplingInput)
            # print('This is samples... ', samples)
            # id = get_event_id()
            # response = {
            #     "samples": samples,
            # }
            # print("Startifies sampling data is ", response)
            samples = sample.values.T.tolist()            
            response = {"samples": samples}
            # return response
            return response

        elif sampling == "quota_sampling":
            
            allocation_type = raw_data.get("allocationType")
            quota_categories = raw_data.get("quota_categories")
            quotaSamplingInput = {
                "population_units": Yi,
                "population_size": population_size,
                "unit": allocation_type,
                # ========
                'populations': population_sizes,
                'sample_size': sample_size,
                "sam": df,
                "quota_categories": quota_categories,
            }
            sample = dowellQuotaSampling(quotaSamplingInput)
            print('This is sample ', sample)
            # quota_sample = df.head(sample_size)
            # sample =quota_sample
            # id = get_event_id()
            samples = sample.values.T.tolist() 
                       
            # response = {"samples": samples}
            response = {"samples": samples}
            return response

        elif sampling == "pps_sampling":
            size = raw_data.get("size")
            size_column = raw_data.get("size_column")
            ppsSamplingInputs = {
                "population_units": Yi,
                "population_size": population_sizes,
                "size": size,
                # ===========
                'populations': population_sizes,
                'sample_size': sample_size,
                "sam": df,
                "size_column": size_column
            }
            # samples, process_time = dowellppsSampling(ppsSamplingInputs)
            sample = dowellppsSampling(ppsSamplingInputs)
            samples = sample.values.T.tolist() 
            return {"samples": samples}
        
        elif sampling == "snowball_sampling":
            error = raw_data.get("error")
            reference = raw_data.get("reference")
            sample_size = dowellSampleSize(int(population_size), float(error))
            population_units = snowball_sampling_data()
            population_size = len(snowball_sampling_data())
            snowballSamplingInputs = {
                "population_size": population_sizes,
                "sample_size": sample_size,
                "population_units": snowball_sampling_data(),
                "reference": reference,
            }
            samples = dowellSnowballSampling(
                # population_units, population_size, sample_size, reference
                snowballSamplingInputs
            )
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
        

        # Choose the sampling method for the current stage
        # sampling_method = dowellindex()

        # Determine the number of units to be selected in the current stage

        # Check if the user entered "0" for the current stage
        if sampling_method[i] == 0:
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
            sample = dowellppsSampling(body)
        # Check if the selected sampling method is Snowball Sampling
        elif sampling_method[i] == 11:
            sample = dowellSnowballSampling(body)
        # Check if the selected sampling method is Quota Sampling
        elif sampling_method[i] == 12:
            sample = dowellQuotaSampling(body)
        else:
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
