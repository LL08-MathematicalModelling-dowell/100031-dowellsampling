from .sampleSize import dowellSampleSize
from .simpleRandomSampling import dowellSimpleRandomSampling
from .allocation import dowellEqualAllocation, dowellProportionalAllocation
import requests
import json
import pandas as pd

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
  
  sample_size = stratifiedSamplingInput['sample_size']
  strata_variable = stratifiedSamplingInput['strata_variable']
  print('star ', strata_variable)
  df = pd.DataFrame(stratifiedSamplingInput['sam'])
  print(df)
  e = stratifiedSamplingInput['e']
  allocationType = stratifiedSamplingInput['allocationType']
  samplingType = stratifiedSamplingInput['samplingType']
  if len(samplingType) == 0:
    sample_size_per_stratum = sample_size
    stratified_sample = df.groupby(strata_variable, group_keys=False).apply(lambda x: x.sample(sample_size_per_stratum))
    return stratified_sample
  else:
    
    print('This is sampling type ', type(samplingType))
    insertedId = stratifiedSamplingInput['insertedId']
    replacement = stratifiedSamplingInput['replacement']

    Yi = stratifiedSamplingInput['Yi']
    N = int(stratifiedSamplingInput['populations'])
    population_sizes = int(stratifiedSamplingInput['populations'])
    
    data = stratifiedSamplingInput['sam']
    sample_size = stratifiedSamplingInput['sample_size']
    print('Method ', samplingType)
    if (not samplingType):
      print('its none')
    else:
      print('not none')
  
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
    simpleRandomSamplingInput = {
              'Yi': Yi,
              'N': int(N),
              'n': n,
              'method': stratifiedSamplingInput['samplingType'],
              # =====
              'populations': population_sizes,
              'sample_size': sample_size,
              'sam': data,
          }
    simpleRandomSamplingOutput = dowellSimpleRandomSampling(simpleRandomSamplingInput)
    if simpleRandomSamplingOutput['status'] == True:
      stratifiedSamplingOutput['sampleUnits'] = simpleRandomSamplingOutput['sampleUnits']
    else:
      stratifiedSamplingOutput['message'] = simpleRandomSamplingOutput['message']
      
      
    
    return stratifiedSamplingOutput