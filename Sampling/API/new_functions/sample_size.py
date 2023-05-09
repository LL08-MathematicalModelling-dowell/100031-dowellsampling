import math


# def dowell_sample_size(N, k, Ni, margin_of_error, confidence_level):
#     z = 1.96  # Z-score for 95% confidence level
#     p_values = [Ni[i]/N for i in range(k)]
#     if 0 in p_values:
#         print("Skipping strata with zero population size")
#         k = sum(1 for p in p_values if p > 0)
#         Ni = [Ni[i] for i in range(k) if p_values[i] > 0]
#         p_values = [Ni[i]/N for i in range(k)]
#     n = sum([Ni[i]*z**2*p_values[i]*(1-p_values[i])/((Ni[i]-1)*margin_of_error**2+z**2*p_values[i]*(1-p_values[i])) for i in range(k)])
#     return math.ceil(n)

def dowellSampleSize(N, e):
    n = int(N / (1 + N * e * e))
    if n > 3 and n < 500:
        return n
    else:
        return(f"Sample size is not adequate")