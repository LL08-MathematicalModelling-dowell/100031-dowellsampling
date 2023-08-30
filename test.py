def dowellQuotaSampling(Yi, N, n, k, Ni, ni):
    # Yi: List of population units
    # N: Total population size
    # n: Sample size
    # k: Number of quotas
    # Ni: Population quota for each quota
    # ni: Sample quota for each quota
    
    quotas = []  # List to store sampled units from each quota
    
    # Divide the population into k quotas and sample from each quota
    for _ in range(k):
        quota = []  # List to store sampled units for this quota
        
        # Select ni sample units from each quota
        for _ in range(ni):
            if len(Yi) == 0:
                print("Insufficient population units.")
                break
            
            # Take the first Ni units from Yi for this quota
            units = Yi[:Ni]
            
            # Remove the selected units from Yi
            Yi = Yi[Ni:]
            
            quota.extend(units)
        
        quotas.append(quota)
        
    return quotas

# Example usage
Yi = ['unit1', 'unit2', 'unit3', 'unit4', 'unit5', 'unit6', 'unit7', 'unit8', 'unit9', 'unit10']
N = len(Yi)
n = 20
k = 3
Ni = 3
ni = 2

sampled_quotas = dowellQuotaSampling(Yi, N, n, k, Ni, ni)
for idx, quota in enumerate(sampled_quotas, start=1):
    print(f"Sampled units for Quota {idx}: {quota}")
