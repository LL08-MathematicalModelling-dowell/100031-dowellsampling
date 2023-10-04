
from .geometricalApproach import dowellGeometricalFunction
from .randomGeneration import dowellRandomGeneration
from .mechanicalRandomisation import dowellRandomTable
from random import shuffle

def dowellSimpleRandomSampling(simpleRandomSamplingInput):
    Yi = simpleRandomSamplingInput['Yi']
    N = simpleRandomSamplingInput['N']
    n = simpleRandomSamplingInput['n']
    method = simpleRandomSamplingInput['method']
    # print(Yi)
    # lengths = [len(item) for sublist in Yi for item in sublist]
    # variance = pvariance(lengths)
    variance = 0.23
    simpleRandomSamplingOutput = {
        'status': True
    }
    if variance > 1:
        simpleRandomSamplingOutput['message'] = "Simple random sampling cannot be used"
        simpleRandomSamplingOutput['status'] = False
    else:
        if method == 'geometricalApproach':
            simpleRandomSamplingOutput['sampleUnits'] = dowellGeometricalFunction(N, n, Yi)
        elif method == 'mechanicalRandomisation':
            simpleRandomSamplingOutput['sampleUnits'] = dowellRandomTable(N, n, Yi)
        elif method == 'randomNumberGeneration':
            simpleRandomSamplingOutput['sampleUnits'] = dowellRandomGeneration(N, n, Yi)
        else:
            simpleRandomSamplingOutput['message'] = f'{method} is not a valid method. Select a valid method from geometricalApproach, mechanicalRandomisation, or randomNumberGeneration'
            simpleRandomSamplingOutput['status'] = False
        shuffle(Yi)
    return simpleRandomSamplingOutput