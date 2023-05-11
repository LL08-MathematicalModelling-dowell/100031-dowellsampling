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

  Yi = stratifiedSamplingInput['Yi']
  N = len(Yi)
  for i in range(len(Yi[0])):
    stratas.append(i)
  k = len(stratas)
  if replacement == True:
    for i in stratas:
        tempList = []
        for j in range(len(Yi)):
            tempList.append(Yi[j][i])
        allStratas[i] = tempList
  elif replacement == False:
    for i in stratas:
        tempSet = set()
        for j in range(len(Yi)):
            tempSet.add(Yi[j][i])
        allStratas[i] = list(tempSet)
  else:
    stratifiedSamplingOutput['message'] = f'{replacement} is not a valid option for replacement, select either True or False'

  n = dowellSampleSize(N, e)
  if isinstance(n, int):
    for i in range(1, k+1):
      if allocationType == 'equal':
        ni[stratas[i-1]] = dowellEqualAllocation(n, k)
      
      elif allocationType == 'proportional':
        Ni = len(allStratas[stratas[i-1]])
        ni[stratas[i-1]] = dowellProportionalAllocation(N, n, Ni)
      
      else:
        stratifiedSamplingOutput['message'] = f'{allocationType} is not a valid allocation type, select either equal or proportional allocation type'
  
  else:
    stratifiedSamplingOutput['message'] = n

  simpleRandomSamplingOutput = dowellSimpleRandomSampling(n, N, Yi, samplingType)
  if simpleRandomSamplingOutput['status'] == True:
    stratifiedSamplingOutput['sampleUnits'] = simpleRandomSamplingOutput['sampleUnits']
  else:
    stratifiedSamplingOutput['message'] = simpleRandomSamplingOutput['message']

  return stratifiedSamplingOutput