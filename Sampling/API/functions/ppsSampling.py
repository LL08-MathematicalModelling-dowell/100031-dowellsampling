import random
from API.functions.randomGeneration import dowellRandomGeneration
from API.functions.sampleSize import dowellSampleSize
import time
import json
import pandas as pd

def dowellppsSampling(ppsSamplingInputs):
    population = ppsSamplingInputs['populations']
    sample_size = ppsSamplingInputs['sample_size']
    size_column = ppsSamplingInputs["size_column"]
    dff = ppsSamplingInputs['sam']
    df = pd.DataFrame(dff)
    
    k = df[size_column].str.replace(',', '').astype(int)
    print('Here... also',  k)
    
    
    # df[size_column] = pd.to_numeric(df[size_column], errors='coerce')

    # # Print rows with NaN values in the 'Salary' column
    # print('what' ,df[df[size_column].isna()])
    total_salary =  df[size_column].sum() 
    print('kdkd ', total_salary)
    
    
    
    probabilities = k / k.sum()
    print('Probab ===> ', probabilities)
    # Perform sampling based on the calculated probabilities
    sampled_indices = probabilities.sample(n=sample_size, replace=True, weights=probabilities).index
    
    # Select sampled rows from the DataFrame
    sampled_data = df.loc[sampled_indices]
    
    # print('Sampled data ', sampled_data)
    return sampled_data

    # population_units = ppsSamplingInputs['population_units']
    # population_units = ppsSamplingInputs["population_units"]
    # population_size = ppsSamplingInputs['population_size']
    # sample_size = dowellSampleSize(population_size, e=0.05)
    # # size = [ppsSamplingInputs['size']]
    # size = [1, 2, 3, 4, 5]


    # # Check if the population units vary considerably in size.
    # if len(set(size)) == 1:
    #     print("Population units do not vary considerably in size.")
    #     return []

    # # Use Lahiri method to draw sample. 
    # #random generation method retruning list which isnt comparable to int
    # selected_units = []
    # for _ in range(sample_size):
    #     i = random.randint(1, population_size)
    #     j = random.randint(1, max(size))
    #     if 1 <= i <= population_size and 1 <= j <= max(size):
    #         selected_units.append(population_units[i - 1])
    #     else:
    #         print("Selected random numbers are not appropriate")
    # print(selected_units,"sele")
    # process_time = 0.5
    # return selected_units ,process_time

