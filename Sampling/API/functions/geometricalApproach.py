from random import randrange
import random


def dowellGeometricalFunction(N, n, Yi, data, sample_sizes):
    sampleUnits = []
    required_columns = {'latitude', 'longitude'}
    
    if not required_columns.issubset(data.columns):
        return "Data must contain 'latitude' and 'longitude' columns for geometrical sampling."
    else:
        lower_case_columns = [col.lower() for col in data.columns]

        lat_min, lat_max = lower_case_columns['latitude'].min(), lower_case_columns['latitude'].max()
        lon_min, lon_max = lower_case_columns['longitude'].min(), lower_case_columns['longitude'].max()

        random_lat = random.uniform(lat_min, lat_max)
        random_lon = random.uniform(lon_min, lon_max)

        selected_rows = data[(data['latitude'] == random_lat)
                            & (data['longitude'] == random_lon)]

        # inscribe the circle randomly by starting from a random index

        start = randrange(0, N)
        print('This is the start ', start)
        Yi = Yi[start:] + Yi[:start]
        print('This is Yi ', Yi)
        # partition the population list into 3 parts corresponding to the areas
        # where the triangle touches the circle x, y and z are the three regions
        # in which the triangle will rotate
        partition = N // 3
        x, y, z = (
            Yi[:partition],
            Yi[partition: (2 * partition)],
            Yi[(2 * partition):],
        )
        # check if lists x, y, and z have at least one element
        if len(x) > 0 and len(y) > 0 and len(z) > 0:
        
            for _ in range(n // 3):
                # check if indices are within the bounds of the lists
                if len(x) > 0 and len(y) > 0 and len(z) > 0:
                    sampleUnits.append([x[0], y[0], z[0]])
                    # rotate by 1 value
                    x = x[1:] + x[:1]
                    y = y[1:] + y[:1]
                    z = x[1:] + z[:1]
                else:
                    return []  # or handle the error condition as per your requirements
            return sampleUnits
        else:
            return "Please decrease or increase the value of 'N' to ensure at least 3 units in each partition."
