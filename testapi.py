import requests
import json

# Define the input parameters for the API function
input_params = {
    'N': 230,
    'n': 30,
    'k': 6,
    'Ni': [40, 50, 70, 20, 25, 25],
    'ni': [5, 5, 5, 5, 5, 5],
    'Yi': [10, 20, 30, 40, 50, 60]
}

# Make the POST request to the API endpoint
url = 'http://localhost:8000/API/stratified_sampling/'
headers = {'Content-Type': 'application/json'}
response = requests.post(url, json=input_params, headers=headers)

# Print the JSON response
print(response)
