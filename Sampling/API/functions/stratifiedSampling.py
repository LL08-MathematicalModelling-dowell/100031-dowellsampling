'''
Population Units - Yi
Population Size - N
Sample Size - n
Number of Stratas - k
Population Strata Size - Ni
Stratum Sample Size - ni
Error - e
Allocation Type - allocationType
Replacement - replacement
Method - method
'''
from API.functions.testDatabase import databaseTwo, databaseOne
from API.functions.sampleSize import dowellSampleSize
from API.functions.simpleRandomSampling import dowellSimpleRandomSampling
from API.functions.allocation import dowellEqualAllocation, dowellProportionalAllocation
import requests
import json

def populationUnits(insertedId):

  url = "http://100061.pythonanywhere.com/api/"

  payload = json.dumps({
    "inserted_id": insertedId,
    })

  headers = {
    'Content-Type': 'application/json'
    }

  response = requests.request("POST", url, headers=headers, data=payload).json()
  Yi = response['classifiedData']

  return Yi

def dowellStratifiedSampling(stratifiedSamplingInput):

  stratifiedSamplingOutput = {}
  allStratas = {}
  ni = {}
  stratas = []

  e = stratifiedSamplingInput['e']
  allocationType = stratifiedSamplingInput['allocationType']
  samplingType = stratifiedSamplingInput['samplingType']
  insertedId = stratifiedSamplingInput['insertedId']
  replacement = stratifiedSamplingInput['replacement']

  # Yi = populationUnits(insertedId)  
  Yi = databaseTwo()

  N = len(Yi)

  for i in  Yi[0].keys():
    stratas.append(i)

  k = len(stratas)

  if(replacement == True):

    for i in stratas:
        tempList = []
        for j in Yi:
            tempList.append(j[i])
        allStratas[i] = tempList

  elif(replacement == False):
    for i in stratas:
        tempSet = set()
        for j in Yi:
            tempSet.add(j[i])
        allStratas[i] = list(tempSet)

  else:
    stratifiedSamplingOutput['message'] = f'{replacement} is not a valid option for replacement, select either True or False'

  n = dowellSampleSize(N, e)
  
  if(type(n)== int):

    for i in range(1, k+1):
      
      if(allocationType == 'equal'):
        ni[stratas[i-1]] = dowellEqualAllocation(n, k)
      
      elif(allocationType == 'proportional'):
        Ni = len(allStratas[stratas[i-1]])
        ni[stratas[i-1]] = dowellProportionalAllocation(N, n, Ni)
      
      else:
        stratifiedSamplingOutput['message'] = f'{allocationType} is not a valid allocation type, select a either equal or proportional allocation type'
  
  else:
     stratifiedSamplingOutput['message'] = n

  simpleRandomSamplingOutput = dowellSimpleRandomSampling(n, N, Yi )
  if(simpleRandomSamplingOutput['status'] == True):
    stratifiedSamplingOutput['sampleUnits'] = simpleRandomSamplingOutput['sampleUnits']
  else:
    stratifiedSamplingOutput['message'] = simpleRandomSamplingOutput['message']

  return stratifiedSamplingOutput


# dowellStratifiedSampling({
#   'e': 0.1,
#   'insertedId': "",
#   'samplingType':"",
#   'allocationType': "proportional",
#   'replacement' : True,
#   'method': 'proportoinal',
  
# })