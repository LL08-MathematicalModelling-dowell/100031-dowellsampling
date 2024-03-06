def dowellSnowballSampling(snowballSamplingInputs):
    # Initialize the sample with the reference units
    population_units = snowballSamplingInputs["population_units"]
    population_size = snowballSamplingInputs["population_size"]
    sample_size = snowballSamplingInputs["population_size"]
    reference = snowballSamplingInputs["reference"]
    
    sample = set([reference])
    print('sample ', sample)
    queue = [reference]

    while len(sample) < sample_size and queue:
        unit = queue.pop(0)
        print('Units ', unit)
        connections = [x["connections"] for x in population_units if x["name"] == unit][0]
        for connection in connections:
            if connection not in sample:
                sample.add(connection)
                queue.append(connection)

    return list(sample)