import requests

def processApikey(api_key, api_service):
    url = f'https://100105.pythonanywhere.com/api/v3/process-services/?type=api_service&api_key={api_key}'
    payload = {
        "service_id" : api_service
    }
    response = requests.post(url, json=payload)
    return response.text
