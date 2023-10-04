
def dowellProportionalAllocation(N, n, Ni): 
    ni = int((Ni * n) / N)
    return ni

def dowellEqualAllocation(n, k):
    ni = int(n / k)
    return ni