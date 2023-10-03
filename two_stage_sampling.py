def dowelltwostagesampling(number_of_stages, sampling_method, body):
    # Define the number of stages
    S = number_of_stages if number_of_stages != None else 0
    # S = int(input("Enter the number of stages: "))

    if number_of_stages not in [1, 2]:
        raise ValueError("Number of stages must be 1 or 2.")

    # List to store the selected units at each stage
    sample_values = []

    # Iterate over each stage
    i = 0
    while i < S:
        print(sampling_method[i])

        print(f"\nStage {i}:")

        # Choose the sampling method for the current stage
        # sampling_method = dowellindex()

        # Determine the number of units to be selected in the current stage

        # Check if the user entered "0" for the current stage
        if sampling_method[i] == 0:
            print("Sampling stopped.")
            break
        # Check if the selected sampling method is Simple Random Sampling
        elif sampling_method[i] == 1 or sampling_method[i] == 2:
            sample = dowellSimpleRandomSampling(body)
        # Check if the selected sampling method is Stratified Sampling
        elif sampling_method[i] == 3 or sampling_method[i] == 4:
            sample = dowellStratifiedSampling(body)
        # Check if the selected sampling method is Systematic Sampling
        elif sampling_method[i] == 5 or sampling_method[i] == 6:
            sample = dowellSystematicSampling(body)
        # Check if the selected sampling method is Cluster Sampling
        elif sampling_method[i] == 7:
            sample = dowellClusterSampling(body)
        # Check if the selected sampling method is Purposive Sampling
        elif sampling_method[i] == 8:
            sample = dowellPurposiveSampling(body)
        # Check if the selected sampling method is PPS Sampling
        elif sampling_method[i] == 9 or sampling_method[i] == 10:
            print(body)
            sample = dowellppsSampling(body)
        # Check if the selected sampling method is Snowball Sampling
        elif sampling_method[i] == 11:
            sample = dowellSnowballSampling(body)
        # Check if the selected sampling method is Quota Sampling
        elif sampling_method[i] == 12:
            sample = dowellQuotaSampling(body)
        else:
            print("Invalid sampling method.")
            continue
        i += 1
        # Add the selected sample to the list of sample values
        sample_values.append(sample)

    # Process time
    process_time = time.process_time()

    # Permutation chosen
    permutation_chosen = None  # Placeholder for permutation chosen

    return sample_values, process_time, permutation_chosen