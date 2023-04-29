from API.functions.sampleSize import dowellSampleSize
from API.functions.geometricalApproach import dowellGeometricalFunction
from API.functions.randomGeneration import dowellRandomGeneration
from API.functions.mechanicalRandomisation import dowellRandomTable
from statistics import pvariance
from random import shuffle

def dowellSimpleRandomSampling(n, N, Yi, method):
    variance = pvariance(Yi)
    simpleRandomSamplingOutput = {
        'status': True
    }
    if variance > 1:
        simpleRandomSamplingOutput['message'] = "Simple random sampling can not be used"
        simpleRandomSamplingOutput['status'] = False
    else:
        if(method == 'geometricalApproach'):
            simpleRandomSamplingOutput['sampleUnits'] = dowellGeometricalFunction(N, n, Yi)
        elif(method == 'mechanicalRandomisation'):
            simpleRandomSamplingOutput['sampleUnits'] = dowellRandomTable(N, n, Yi)
        elif(method == 'randomNumberGeneration'):
            simpleRandomSamplingOutput['sampleUnits'] = dowellRandomGeneration(N, n, Yi)
        else:
            simpleRandomSamplingOutput['message'] = f'{method} is not a valid method. Select a valid method from geometricalApproach, mechanicalRandomisation or randomNumberGeneration'
            simpleRandomSamplingOutput['status'] = False
        shuffle(Yi)
    return simpleRandomSamplingOutput