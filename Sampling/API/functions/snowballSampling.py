import random

def dowellSnowballSampling(population_units, population_size, sample_size, reference):
    sample = []
    connections = set()

    # Create a connections attribute for each unit.
    for unit in population_units:
        unit["connections"] = []

    # Select the first unit to be included in the sample.
    unit = None
    for person in population_units:
        if person["name"] == reference:
            unit = person
            break

    if unit is None:
        return "Reference person not found in the population_units."

    sample.append(unit)
    connections.add(unit["name"])

    # Iterate until the sample size is reached.
    while len(sample) < sample_size:
        # Find a connection from the current unit.
        connection = None
        for unit_connection in unit["connections"]:
            if unit_connection not in connections:
                connection = unit_connection
                break

        # If no connection was found, return an error message.
        if connection is None:
            return "Could not find a connection from the current unit."

        # Add the connection to the set of connections and the sample.
        connections.add(connection)
        sample.append(unit)
        for person in population_units:
            if person["name"] == connection:
                unit = person
                break

        sample.append(unit)

    return sample