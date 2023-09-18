from API.functions.sampleSize import dowellSampleSize

def dowellPurposiveSampling(purposeiveSamplingInput):
    N = purposeiveSamplingInput['populationSize']
    e = purposeiveSamplingInput['error']
    n = dowellSampleSize(N, e)
    unit = purposeiveSamplingInput['unit']
    Yi = purposeiveSamplingInput['Yi']
    sample_values = []

    unit_copy = Yi[:]
    print("unit copy", unit_copy)
    while len(sample_values) < n:
        if len(unit_copy) == 0:
            print("Insufficient units in the 'unit' list.")
            break

        unit = unit_copy.pop(0)
        # print("unit", unit)
        if unit in purposeiveSamplingInput['unit']:
            sample_values.append(unit)
        else:
            print("Unit not found in the provided unit list. Select another available unit.")

        if len(sample_values) == n:
            break

    return sample_values