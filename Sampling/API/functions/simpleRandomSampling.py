from .sampleSize import dowellSampleSize
from .geometricalApproach import dowellGeometricalFunction
from .randomGeneration import dowellRandomGeneration
from .mechanicalRandomisation import dowellRandomTable
from statistics import pvariance
from random import shuffle

def dowellSimpleRandomSampling(simpleRandomSamplingInput):
    
    Yi = simpleRandomSamplingInput['Yi']
    N = simpleRandomSamplingInput['N']
    n = simpleRandomSamplingInput['n']
    data = simpleRandomSamplingInput['sam']
    
    method = simpleRandomSamplingInput['method']
    
    sample_sizes = simpleRandomSamplingInput['sample_size']
    
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
            
            lower_case_columns = [col.lower() for col in data.columns]
            if 'age' in lower_case_columns and 'gender' in lower_case_columns:
                print('Running ', dowellGeometricalFunction(N, n, Yi, data, sample_sizes))
                simpleRandomSamplingOutput['sampleUnits'] = dowellGeometricalFunction(N, n, Yi, data, sample_sizes)
            else:
                
                simpleRandomSamplingOutput['message'] = f'{method} is not a valid method. Select a valid method from geometricalApproach, mechanicalRandomisation, or randomNumberGeneration'
                simpleRandomSamplingOutput['status'] = False
                
            # simpleRandomSamplingOutput['sampleUnits'] = dowellGeometricalFunction(N, n, Yi)
        elif method == 'mechanicalRandomisation':
            
            simpleRandomSamplingOutput['sampleUnits'] = dowellRandomTable(N, n, Yi, sample_sizes)
        elif method == 'randomNumberGeneration':
            simpleRandomSamplingOutput['sampleUnits'] = dowellRandomGeneration(N, n, Yi, sample_sizes)
            
        else:
            simpleRandomSamplingOutput['message'] = f'{method} is not a valid method. Select a valid method from geometricalApproach, mechanicalRandomisation, or randomNumberGeneration'
            simpleRandomSamplingOutput['status'] = False
            
        shuffle(Yi)
    
    return simpleRandomSamplingOutput