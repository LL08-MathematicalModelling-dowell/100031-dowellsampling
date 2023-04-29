import time
from API.new_functions.proportionalallocation import dowellproportional_allocation
from API.new_functions.randomsampling import dowellrandomsampling

# Dowell's stratified sampling method
def dowellstratifiedsampling(Yi, N, n, k, Ni_list, ni_list):
    # Check that the sum of ni_list is less than or equal to N and none of its values are negative
    if sum(ni_list) > N:
        raise ValueError("Error: Sum of sample sizes is greater than population size.")
    elif any(x < 0 for x in ni_list):
        raise ValueError("Error: Sample size cannot be negative.")
    else:
        start_time = time.time()
        sample_units = []

        for i in range(k):
            stratum = Yi[Ni_list[i]:Ni_list[i+1]]
            ni = ni_list[i]

            # Check that ni is not larger than the population size of the stratum and ni is not negative
            if ni > len(stratum):
                ni = len(stratum)
            elif ni < 0:
                ni = 0

            # Allocate sample units using Dowell's proportional allocation method
            sample_unit = dowellproportional_allocation(stratum, ni)

            # Sample sample_unit[i] units from stratum[i] using Dowell's random sampling method
            for j in range(len(sample_unit)):
                if sample_unit[j] > 0:
                    s = dowellrandomsampling(stratum[j:], sample_unit[j])
                    sample_units.extend(s)

        end_time = time.time()
        process_time = end_time - start_time

        return (sample_units, process_time)