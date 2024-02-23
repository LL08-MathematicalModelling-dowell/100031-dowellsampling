from API.functions.sampleSize import dowellSampleSize
from API.functions.purposiveSampling import dowellPurposiveSampling
import time
import pandas as pd


def dowellQuotaSampling(quotaSamplingInput):
    
    # Yi,population_size,allocation_type,
    df = quotaSamplingInput['sam']
    
    quota_categories = quotaSamplingInput['quota_categories']
    
    
    sampled_data = pd.DataFrame(columns=df.columns)
    print('here it is ', sampled_data)
    
    # Performing quota sampling
    for category, quotas in quota_categories.items():

        for category_value, quota in quotas.items():
            # Select observations matching the category value
            category_data = df[df[category] == category_value]
            # Sample observations from the category data
            sampled_category_data = category_data.sample(n=quota, replace=True)
            # Add sampled data to the sampled_data DataFrame
            sampled_data = pd.concat([sampled_data, sampled_category_data])
            # print('fdd ', sampled_data)

    print('This is quota ', sampled_data)
    # Reset index of sampled data
    sampled_data.reset_index(drop=True, inplace=True)
    print('ff ', sampled_data)
        
    return sampled_data
    
    
    
    
    
    
    
    
    # process_time = 0
    # n = dowellSampleSize(7, e=0.05)
    # quotas = []
    # sample_units = []
    # purposive_input = {}
    # # Yi = Yi
    # all_quotas = {}
    # ni = {}
    # N = population_size

    # for i in range(len(Yi[0])):
    #     quotas.append(i)
    # k = len(quotas)

    # for i in quotas:
    #     tempList = []
    #     for j in range(len(Yi)):
    #         tempList.append(Yi[j])
    #     all_quotas[i] = tempList

    # if isinstance(n, int):
    #     for i in range(1, k+1):
    #         Ni = len(all_quotas[quotas[i-1]])
    #         ni[quotas[i-1]] = dowellSampleSize(N, n, Ni)
    #         purposive_input["N"] = N
    #         purposive_input["e"] = 0.05
    #         purposive_input["Yi"] = Yi
    #         purposive_input["unit"] = None
    #         sample = dowellPurposiveSampling(purposive_input)
    #         sample_units.append(sample)

    # process_time = time.process_time()

    # return(sample_units)