import json
import math
import time
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from API.functions.API_Key_System import processApikey
import random
from .functions.sample_size import calculate_sample_size

@csrf_exempt
def sample_size(request):
    if (request.method=="POST"):
        data=json.loads(request.body)
        return calculate_sample_size(data)
    else:
        return HttpResponse("Method Not Allowed")

@csrf_exempt
def sample_size_api(request, api_key):
    if (request.method=="POST"):
        data=json.loads(request.body)
        validate_api_count = processApikey(api_key, "DOWELL10032")
        data_count = json.loads(validate_api_count)
        if data_count['success'] :
            if data_count['total_credits'] >= 0:
                return calculate_sample_size(data)
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
def health_check(request):
    print('Hello World!')
    if (request.method=="GET"):
        return JsonResponse({"status": "ok"})