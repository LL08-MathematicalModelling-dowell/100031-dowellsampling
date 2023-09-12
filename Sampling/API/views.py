import os
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
from API.functions.quotaSampling import dowellQuotaSampling
from API.functions.ppsSampling import dowellppsSampling


@csrf_exempt
def get_event_id():
    url = "https://uxlivinglab.pythonanywhere.com/create_event"

    data = {
        "platformcode": "FB",
        "citycode": "101",
        "daycode": "0",
        "dbcode": "pfm",
        "ip_address": "192.168.0.41",
        "login_id": "lav",
        "session_id": "new",
        "processcode": "1",
        "location": "22446576",
        "objectcode": "1",
        "instancecode": "100051",
        "context": "afdafa ",
        "document_id": "3004",
        "rules": "some rules",
        "status": "work",
        "data_type": "learn",
        "purpose_of_usage": "add",
        "colour": "color value",
        "hashtags": "hash tag alue",
        "mentions": "mentions value",
        "emojis": "emojis",
        "bookmarks": "a book marks",
    }

    r = requests.post(url, json=data)
    if r.status_code == 201:
        return json.loads(r.text)
    else:
        return json.loads(r.text)["error"]


@csrf_exempt
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
                n = dowellSampleSize(int(population_size), float(e))
                simpleRandomSamplingInput = {
                    "insertedId": inserted_id,
                    "Yi": Yi,
                    "N": int(population_size),
                    "e": float(e),
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


@csrf_exempt
def systematic_sampling(request):
    if request.method == "POST":
        json_data = request.POST.get("json_data")  # Retrieve the JSON data as a string
        print("json_data", json_data)
        try:
            # Parse JSON data from the request body
            json_data = json.loads(json_data)
            inserted_id = json_data.get("insertedId")
            population_size = json_data.get("populationSize")
            result = json_data.get("result")
            data_type = json_data.get("data")

            if data_type == "api":
                Yi = get_YI_data_new()
            elif data_type == "upload":
                uploaded_file = request.FILES.get("file")
                if uploaded_file:
                    df = pd.read_excel(uploaded_file)
                    list_of_lists = df.values.T.tolist()
                    Yi = list_of_lists
                else:
                    return JsonResponse({"error": "No file uploaded."})
            elif data_type == "link":
                excel_link = json_data.get("link")
                if excel_link:
                    df = pd.read_excel(excel_link)
                    list_of_lists = df.values.T.tolist()
                    Yi = list_of_lists
                else:
                    return JsonResponse({"error": "No link provided."})
            else:
                return JsonResponse({"error": "Invalid data option."})

            systematicSamplingInput = {
                "insertedId": inserted_id,
                "population": Yi,
                "population_size": population_size,
            }

            samples = dowellSystematicSampling(systematicSamplingInput)
            response = {"samples": samples}

            return JsonResponse(response, safe=False)

        except Exception as e:
            return JsonResponse({"error": str(e)})

    return JsonResponse({"error": "Invalid request method."})


@csrf_exempt
def simple_random_sampling(request):
    if request.method == "POST":
        json_data = request.POST.get("json_data")
        try:
            data = json.loads(json_data)
            print(data)
            inserted_id = data.get("insertedId")
            N = data.get("populationSize")
            e = data.get("e")
            method = data.get("samplingType")
            n = dowellSampleSize(int(N), float(e))
            result = data.get("result")
            data_type = data.get("data")

            if data_type == "api":
                Yi = get_YI_data_new()

            elif data_type == "upload":
                uploaded_file = request.FILES.get("file")
                if uploaded_file:
                    df = pd.read_excel(uploaded_file)
                    list_of_lists = df.values.T.tolist()
                    Yi = list_of_lists
                else:
                    return JsonResponse({"error": "No file uploaded."})
            elif data_type == "link":
                excel_link = data.get("link")
                if excel_link:
                    df = pd.read_excel(excel_link)
                    list_of_lists = df.values.T.tolist()
                    Yi = list_of_lists
                else:
                    return JsonResponse({"error": "No link provided."})
            else:
                return JsonResponse({"error": "Invalid data option."})

            simpleRandomSamplingInput = {
                "insertedId": inserted_id,
                "Yi": Yi,
                "N": int(N),
                "e": float(e),
                "method": method,
                "n": n,
            }

            samples = dowellSimpleRandomSampling(simpleRandomSamplingInput)
            response = {"samples": samples["sampleUnits"]}

            return JsonResponse(response, safe=False)

        except Exception as e:
            return JsonResponse({"error": str(e)})

    return JsonResponse({"error": "Invalid request method."})


@csrf_exempt
def purposive_sampling(request):
    if request.method == "POST":
        try:
            json_data = request.POST.get("json_data")
            print("json_data", json_data)
            data = json.loads(json_data)
            print(data)
            inserted_id = data.get("insertedId")
            unit = data.get("unit")
            e = data.get("e")
            N = data.get("N")
            result = data.get("result")

            if data["data"] == "api":
                Yi = get_YI_data()  # Make sure you have a function for this
            elif data["data"] == "upload":
                uploaded_file = request.FILES.get("file")
                if uploaded_file:
                    df = pd.read_excel(uploaded_file)
                    list_of_lists = df.values.T.tolist()
                    Yi = list_of_lists
                else:
                    return JsonResponse({"error": "No file uploaded."})
            elif data["data"] == "link":
                excel_link = data.get("link")
                if excel_link:
                    df = pd.read_excel(excel_link)
                    list_of_lists = df.values.T.tolist()
                    Yi = list_of_lists
                else:
                    return JsonResponse({"error": "No link provided."})
            else:
                return JsonResponse({"error": "Invalid data option."})

            new_yi = sum(Yi, [])
            purposiveSamplingInput = {
                "insertedId": inserted_id,
                "Yi": new_yi,
                "unit": unit,
                "e": float(e),
                "N": int(N),
            }

            samples = dowellPurposiveSampling(purposiveSamplingInput)
            id = get_event_id()  # Make sure you have a function for this
            response = {"event_id": id["event_id"], "samples": samples["sampleUnits"]}

            return JsonResponse(response, safe=False)

        except Exception as e:
            return JsonResponse({"error": str(e)})

    return JsonResponse({"error": "Invalid request method."})


@csrf_exempt
def cluster_sampling(request):
    if request.method == "POST":
        try:
            json_data = request.POST.get("json_data")
            data = json.loads(json_data)

            inserted_id = data.get("insertedId")
            numberOfClusters = data.get("numberOfClusters")
            M = data.get("numberOfClusters")  # Same as numberOfClusters
            N = data.get("populationSize")
            e = data.get("e")
            sizeOfCluster = data.get("sizeOfCluster")
            result = data.get("result")

            if data["data"] == "api":
                Yi = get_YI_data()  # Make sure you have a function for this
            elif data["data"] == "upload":
                uploaded_file = request.FILES.get("file")
                if uploaded_file:
                    df = pd.read_excel(uploaded_file)
                    list_of_lists = df.values.T.tolist()
                    Yi = list_of_lists
                else:
                    return JsonResponse({"error": "No file uploaded."})
            else:
                return JsonResponse({"error": "Invalid data option."})

            clusterSamplingInput = {
                "Yi": Yi,
                "e": float(e),
                "N": int(N),
                "M": int(M),
                "hi": int(sizeOfCluster),  # Using sizeOfCluster as hi
            }

            samples = dowellClusterSampling(clusterSamplingInput)
            id = get_event_id()  # Make sure you have a function for this
            response = {"event_id": id["event_id"], "samples": samples["sampleUnits"]}

            return JsonResponse(response, safe=False)

        except Exception as e:
            return JsonResponse({"error": str(e)})

    return JsonResponse({"error": "Invalid request method."})


@csrf_exempt
def stratified_sampling(request):
    if request.method == "POST":
        try:
            json_data = request.POST.get("json_data")
            data = json.loads(json_data)

            inserted_id = data.get("insertedId")
            allocation_type = data.get("allocationType")
            sampling_type = data.get("samplingType")
            replacement = data.get("replacement")
            populationSize = data.get("populationSize")

            if data["data"] == "api":
                Yi = get_YI_data()  # Make sure you have a function for this
            elif data["data"] == "upload":
                uploaded_file = request.FILES.get("file")
                if uploaded_file:
                    df = pd.read_excel(uploaded_file)
                    list_of_lists = df.values.T.tolist()
                    Yi = list_of_lists
                else:
                    return JsonResponse({"error": "No file uploaded."})
            else:
                return JsonResponse({"error": "Invalid data option."})

            stratifiedSamplingInput = {
                "insertedId": inserted_id,
                "e": 0.1,
                "allocationType": allocation_type,
                "samplingType": sampling_type,
                "replacement": replacement,
                "Yi": Yi,
                "populationSize": populationSize,
            }

            samples = dowellStratifiedSampling(stratifiedSamplingInput)
            id = get_event_id()  # Make sure you have a function for this
            response = {"event_id": id["event_id"], "samples": samples["sampleUnits"]}

            return JsonResponse(response, safe=False)

        except Exception as e:
            return JsonResponse({"error": str(e)})

    return JsonResponse({"error": "Invalid request method."})


@csrf_exempt
def quota_sampling(request):
    if request.method == "POST":
        try:
            json_data = request.POST.get("json_data")
            data = json.loads(json_data)

            inserted_id = data.get("insertedId")
            allocation_type = data.get("allocationType")
            population_size = data.get("populationSize")

            if data["data"] == "api":
                Yi = get_YI_data()  # Make sure you have a function for this
            elif data["data"] == "upload":
                uploaded_file = request.FILES.get("file")
                if uploaded_file:
                    df = pd.read_excel(uploaded_file)
                    list_of_lists = df.values.T.tolist()
                    Yi = list_of_lists
                else:
                    return JsonResponse({"error": "No file uploaded."})
            else:
                return JsonResponse({"error": "Invalid data option."})

            quotaSamplingInput = {
                "population_units": Yi,
                "population_size": population_size,
                "unit": allocation_type,
            }

            samples, process_time = dowellQuotaSampling(**quotaSamplingInput)
            id = get_event_id()
            response = {"event_id": id["event_id"], "samples": samples}

            return JsonResponse(response, safe=False)

        except Exception as e:
            return JsonResponse({"error": str(e)})

    return JsonResponse({"error": "Invalid request method."})


@csrf_exempt
def pps_sampling(request):
    if request.method == "POST":
        try:
            json_data = request.POST.get("json_data")
            data = json.loads(json_data)
            print("data", data)
            inserted_id = data.get("insertedId")
            population_size = data.get("population_size")
            size = data.get("size")

            if data["data"] == "api":
                Yi = get_YI_data_new()
            elif data["data"] == "upload":
                uploaded_file = request.FILES.get("file")
                if uploaded_file:
                    df = pd.read_excel(uploaded_file)
                    list_of_lists = df.values.T.tolist()
                    Yi = list_of_lists
                else:
                    return JsonResponse({"error": "No file uploaded."})
            else:
                return JsonResponse({"error": "Invalid data option."})

            ppsSamplingInputs = {
                "population_units": Yi,
                "population_size": population_size,
                "size": size,
            }
            # print(ppsSamplingInputs)

            samples, process_time = dowellppsSampling(ppsSamplingInputs)
            print(samples)
            # id = get_event_id()  # Make sure you have a function for this
            response = {"samples": samples}
            return JsonResponse({"samples": samples})

        except Exception as e:
            return JsonResponse({"error": str(e)})

    return JsonResponse({"error": "Invalid request method."})
