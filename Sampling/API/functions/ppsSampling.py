import random
from API.functions.randomGeneration import dowellRandomGeneration
from API.functions.sampleSize import dowellSampleSize
import time
import json

def dowellppsSampling(ppsSamplingInputs):
    
    # population_units = ppsSamplingInputs['population_units']
    population_units = ["A", "B", "C", "D", "E"]
    population_size = ppsSamplingInputs['population_size']
    sample_size = dowellSampleSize(population_size, e=0.05)
    # size = [ppsSamplingInputs['size']]
    size = [1, 2, 3, 4, 5]


    # Check if the population units vary considerably in size.
    if len(set(size)) == 1:
        print("Population units do not vary considerably in size.")
        return []

    # Use Lahiri method to draw sample. 
    #random generation method retruning list which isnt comparable to int
    selected_units = []
    for _ in range(sample_size):
        i = random.randint(1, population_size)
        j = random.randint(1, max(size))
        if 1 <= i <= population_size and 1 <= j <= max(size):
            selected_units.append(population_units[i - 1])
        else:
            print("Selected random numbers are not appropriate")
    print(selected_units,"sele")
    process_time = 0.5
    return selected_units ,process_time

