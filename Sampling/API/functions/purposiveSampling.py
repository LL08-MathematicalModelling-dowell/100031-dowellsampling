from API.functions.sampleSize import dowellSampleSize

def dowellPurposiveSampling(purposeiveSamplingInput):
    population =  purposeiveSamplingInput['populations'],
    # population = purposeiveSamplingInput['populations'],
    sample_size = purposeiveSamplingInput['sample_size']
    data = purposeiveSamplingInput["sam"]
    unit = purposeiveSamplingInput['unit']
    print('This is the unit... ', type(unit))
    target_occupations = [unit]
    print('This is the taeget occupation... ', target_occupations)
    
    print('Sample size ', sample_size)
    print('Population type ', type(population))
    if sample_size > purposeiveSamplingInput['populations']:
        print("Insufficient units in the 'unit' list.")
    
    else:
        sample_values = data[data['Occupation'].isin(target_occupations)]
        print('Purposive sampling ', sample_values)
        return sample_values
        
    
    
    # N = purposeiveSamplingInput['populationSize']
    # e = purposeiveSamplingInput['error']
    # n = dowellSampleSize(N, e)
    # unit = purposeiveSamplingInput['unit']
    # Yi = purposeiveSamplingInput['Yi']
    # sample_values = []

    # unit_copy = Yi[:]
    # print("unit copy", unit_copy)
    # while len(sample_values) < n:
    #     if len(unit_copy) == 0:
    #         print("Insufficient units in the 'unit' list.")
    #         break

    #     unit = unit_copy.pop(0)
    #     # print("unit", unit)
    #     if unit in purposeiveSamplingInput['unit']:
    #         sample_values.append(unit)
    #     else:
    #         print("Unit not found in the provided unit list. Select another available unit.")

    #     if len(sample_values) == n:
    #         break

    # return sample_values