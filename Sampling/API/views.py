import json
import requests
import pandas as pd

from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

from API.functions.stratifiedSampling import dowellStratifiedSampling
from API.functions.sampleSize import dowellSampleSize
from API.functions.systematic_sampling import dowellSystematicSampling
from API.functions.simpleRandomSampling import dowellSimpleRandomSampling
from API.functions.clusterSampling import dowellClusterSampling
from API.functions.purposiveSampling import dowellPurposiveSampling
from API.functions.quotaSampling import dowellQuotaSampling
from API.functions.ppsSampling import dowellppsSampling
from API.functions.get_event_id import get_event_id

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


@csrf_exempt
def mainSampling(request):
    if request.method == "POST":
        raw_data = json.loads(request.body.decode("utf-8"))
        print("json_data", raw_data)
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
                    return JsonResponse({"error": "No link provided."})
            else:
                return JsonResponse({"error": "api or link not selected"})

            if sampling == "systematic_sampling":
                systematicSamplingInput = {
                    "insertedId": inserted_id,
                    "population": Yi,
                    "population_size": population_size,
                }
                samples = dowellSystematicSampling(systematicSamplingInput)
                response = {"samples": samples}
                return JsonResponse(response, safe=False)

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
                return JsonResponse(response, safe=False)

            elif sampling == "purposive_sampling":
                error = raw_data.get("error")
                unit = raw_data.get("unit")
                new_yi = sum(Yi, [])
                purposiveSamplingInput = {
                    "insertedId": inserted_id,
                    "Yi": new_yi,
                    "unit": unit,
                    "e": float(error),
                    "N": int(population_size),
                }

                samples = dowellPurposiveSampling(purposiveSamplingInput)
                id = get_event_id()  # Make sure you have a function for this
                response = {
                    "samples": samples["sampleUnits"],
                }
                return JsonResponse(response, safe=False)

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
                id = get_event_id()  # Make sure you have a function for this
                response = {
                    "samples": samples["sampleUnits"],
                }

                return JsonResponse(response, safe=False)

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
                samples = dowellStratifiedSampling(stratifiedSamplingInput)
                id = get_event_id()  # Make sure you have a function for this
                response = {
                    "event_id": id["event_id"],
                    "samples": samples["sampleUnits"],
                }

                return JsonResponse(response, safe=False)

            elif sampling == "quota_sampling":
                allocation_type = raw_data.get("allocationType")
                quotaSamplingInput = {
                    "population_units": Yi,
                    "population_size": population_size,
                    "unit": allocation_type,
                }

                samples, process_time = dowellQuotaSampling(**quotaSamplingInput)
                id = get_event_id()
                response = {"event_id": id["event_id"], "samples": samples}

                return JsonResponse(response, safe=False)

            elif sampling == "pps_sampling":
                size = raw_data.get("size")
                ppsSamplingInputs = {
                "population_units": Yi,
                "population_size": population_size,
                "size": size,
            }
                samples, process_time = dowellppsSampling(ppsSamplingInputs)
                print(samples)
                # id = get_event_id()  # Make sure you have a function for this
                response = {"samples": samples}
                return JsonResponse({"samples": samples})

        except Exception as e:
            return JsonResponse({"error": str(e)})