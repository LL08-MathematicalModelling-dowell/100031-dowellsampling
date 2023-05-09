'''
Population Size - N
Stratum Number - K
Stratum Size - Ni
Sample Size - n
'''
from API.functions.sampleSize import dowellSampleSize
def dowellProportionalAllocation(N, n, Ni): 
    ni = int((Ni * n) / N)
    return ni

def dowellEqualAllocation(n, k):
    ni = int(n / k)
    return ni