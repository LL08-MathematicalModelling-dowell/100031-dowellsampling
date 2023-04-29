import requests

api_url = 'http://localhost:8000/API/get_data/'

response = requests.get(api_url)
if response.status_code == 200:
    json_data = response.json()
    data = json_data['finalOutput']
    print(f'{data}')
else:
    print(f'Request failed with status code {response.status_code}')
