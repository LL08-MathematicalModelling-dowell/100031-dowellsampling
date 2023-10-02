from API.functions.sampleSize import dowellSampleSize
from API.functions.purposiveSampling import dowellPurposiveSampling
import time


def dowellQuotaSampling(Yi,population_size,allocation_type):
    process_time = 0
    n = dowellSampleSize(7, e=0.05)
    quotas = []
    sample_units = []
    purposive_input = {}
    # Yi = Yi
    all_quotas = {}
    ni = {}
    N = population_size

    for i in range(len(Yi[0])):
        quotas.append(i)
    k = len(quotas)

    for i in quotas:
        tempList = []
        for j in range(len(Yi)):
            print(j)
            tempList.append(Yi[j])
        all_quotas[i] = tempList
        print(all_quotas)

    if isinstance(n, int):
        for i in range(1, k+1):
            Ni = len(all_quotas[quotas[i-1]])
            ni[quotas[i-1]] = dowellSampleSize(N, n, Ni)
            purposive_input["N"] = N
            purposive_input["e"] = 0.05
            purposive_input["Yi"] = Yi
            purposive_input["unit"] = None
            sample = dowellPurposiveSampling(purposive_input)
            sample_units.append(sample)

    process_time = time.process_time()

    return(sample_units)