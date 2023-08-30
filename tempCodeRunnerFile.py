input_data = {
    'N': 1000,  # Replace with your desired population size
    'e': 0.05,  # Replace with your desired margin of error
    'Yi': ['unit1', 'unit2', 'unit3'],  # Replace with your population units
    'unit': 'unit1,unit2,unit3',  # Replace with the initial unit list
}

result = dowellPurposiveSampling(input_data)
print("Sampled units:", result)