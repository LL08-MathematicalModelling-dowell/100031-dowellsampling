import requests
import json
import requests

url = "https://100004.pythonanywhere.com/api"
# Define the input parameters for the API function
input_params = {
   "title": "backendtesting",
   "Process_id": 10122,
   "processSequenceId": 16,
   "series": 3,				
   "seriesvalues":{
       "list1":[2,23,5,7,2],
       "list2":[5,5,6,7,10],
       "list3":[11,12,13,14,11],
       "list4":[8,8,7,9,15]
   }
}

headers={'content-type': 'application/json'}
try:
    response=requests.post(url,json=input_params,headers=headers)
    print(response.text)
except:
    print("Error in API call")
