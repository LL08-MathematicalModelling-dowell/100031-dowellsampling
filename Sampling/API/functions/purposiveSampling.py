from API.functions.sampleSize import dowellSampleSize

def dowellPurposiveSampling(purposeiveSamplingInput):
    N = purposeiveSamplingInput['N']
    e = purposeiveSamplingInput['e']
    n = dowellSampleSize(N, e)
    Yi = purposeiveSamplingInput['Yi']
    unit = purposeiveSamplingInput['unit']
    unit = unit.split(",")
    print(n)
    sample_values = []
    unit_copy = unit[:]  # Make a copy of the unit list
    while len(sample_values) < n:
        if len(unit_copy) == 0:
            print("Insufficient units in the 'unit' list.")
            break

        units_inp = unit_copy.pop(0)  # Take the first element from the copied list

        units = units_inp.split(",")

        # Check if selected units are matching with the population units
        for i in units:
            if i not in Yi:
                
                print("Select another available unit")
                break
        else:
            sample_values.append(units)

        if len(sample_values) == n:
            break

    return sample_values