def dowellSnowballSampling(population_units, population_size, sample_size, reference):
    # Initialize the sample with the reference units
    sample = set([reference])
    queue = [reference]

    while len(sample) < sample_size and queue:
        unit = queue.pop(0)
        connections = [x["connections"] for x in population_units if x["name"] == unit][0]
        for connection in connections:
            if connection not in sample:
                sample.add(connection)
                queue.append(connection)

    return list(sample)